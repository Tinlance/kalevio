from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.config import settings
from core.database import get_db
from models.organisation import Organisation, PlanTier
import hashlib, hmac, json, logging

router = APIRouter(tags=["billing"])
logger = logging.getLogger(__name__)

# LemonSqueezy plan ID → PlanTier mapping
# Update these IDs when you create products in LemonSqueezy dashboard
PLAN_MAP = {
    "starter":      PlanTier.FREE,
    "professional": PlanTier.PROFESSIONAL,
    "guardian":     PlanTier.GUARDIAN,
    "mssp":         PlanTier.MSSP,
}

def verify_signature(body: bytes, signature: str) -> bool:
    """Verify LemonSqueezy webhook HMAC-SHA256 signature."""
    if not settings.LEMONSQUEEZY_WEBHOOK_SECRET:
        logger.warning("LEMONSQUEEZY_WEBHOOK_SECRET not set — skipping verification")
        return True
    expected = hmac.new(
        settings.LEMONSQUEEZY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

def get_plan_tier(variant_name: str) -> PlanTier:
    """Map LemonSqueezy variant name to PlanTier."""
    name = variant_name.lower()
    for key, tier in PLAN_MAP.items():
        if key in name:
            return tier
    return PlanTier.PROFESSIONAL  # default for any paid plan

@router.post("/webhook/lemonsqueezy")
async def lemonsqueezy_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle LemonSqueezy webhook events.
    Events handled:
    - order_created       → activate subscription
    - subscription_created → activate subscription
    - subscription_updated → update plan tier
    - subscription_cancelled → downgrade to FREE
    """
    body = await request.body()
    signature = request.headers.get("X-Signature", "")

    if not verify_signature(body, signature):
        logger.warning("Invalid LemonSqueezy webhook signature")
        raise HTTPException(401, "Invalid signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON payload")

    event = payload.get("meta", {}).get("event_name", "")
    data = payload.get("data", {})
    attributes = data.get("attributes", {})

    logger.info(f"LemonSqueezy event: {event}")

    # Extract customer email and variant info
    customer_email = attributes.get("user_email", "")
    variant_name = attributes.get("variant_name", "professional")
    ls_customer_id = str(attributes.get("customer_id", ""))
    ls_order_id = str(data.get("id", ""))

    if not customer_email:
        logger.warning(f"No customer email in event {event}")
        return {"status": "ignored", "reason": "no customer email"}

    # Find org by LemonSqueezy customer ID or create association
    result = await db.execute(
        select(Organisation).where(Organisation.ls_customer_id == ls_customer_id)
    )
    org = result.scalar_one_or_none()

    if event in ("order_created", "subscription_created"):
        plan = get_plan_tier(variant_name)
        if org:
            org.plan_tier = plan
            org.is_active = True
            logger.info(f"Updated org {org.id} to plan {plan}")
        else:
            # New customer — create org record
            import uuid
            org = Organisation(
                id=uuid.uuid4(),
                name=f"Organisation ({customer_email})",
                country_code="EE",
                plan_tier=plan,
                ls_customer_id=ls_customer_id,
                is_active=True,
            )
            db.add(org)
            logger.info(f"Created new org for {customer_email} on plan {plan}")
        await db.commit()
        return {"status": "activated", "plan": plan.value, "email": customer_email}

    elif event == "subscription_updated":
        plan = get_plan_tier(variant_name)
        if org:
            org.plan_tier = plan
            await db.commit()
            logger.info(f"Updated org {org.id} to plan {plan}")
            return {"status": "updated", "plan": plan.value}
        return {"status": "ignored", "reason": "org not found"}

    elif event in ("subscription_cancelled", "subscription_expired"):
        if org:
            org.plan_tier = PlanTier.FREE
            org.is_active = True  # keep active on free tier
            await db.commit()
            logger.info(f"Downgraded org {org.id} to FREE")
            return {"status": "downgraded", "plan": "free"}
        return {"status": "ignored", "reason": "org not found"}

    elif event == "subscription_payment_failed":
        logger.warning(f"Payment failed for customer {ls_customer_id}")
        return {"status": "noted", "event": event}

    else:
        logger.info(f"Unhandled event: {event}")
        return {"status": "ignored", "event": event}

@router.get("/plans")
async def list_plans():
    """Return available plans and pricing."""
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price_eur": 149,
                "interval": "month",
                "features": [
                    "5 incident reports/month",
                    "NIS2 scope checker",
                    "Email notifications",
                    "Basic audit trail",
                ]
            },
            {
                "id": "professional",
                "name": "Professional",
                "price_eur": 499,
                "interval": "month",
                "highlighted": True,
                "features": [
                    "Unlimited incident reports",
                    "AI-generated NIS2/DORA reports",
                    "Evidence vault",
                    "Hash-chained audit trail",
                    "CSIRT auto-notification",
                    "API access",
                ]
            },
            {
                "id": "guardian",
                "name": "Guardian",
                "price_eur": 1499,
                "interval": "month",
                "features": [
                    "Everything in Professional",
                    "Multi-site support",
                    "Advanced dashboards",
                    "Priority support",
                    "Custom integrations",
                ]
            },
            {
                "id": "mssp",
                "name": "MSSP",
                "price_eur": 3500,
                "interval": "month",
                "features": [
                    "Everything in Guardian",
                    "White-label options",
                    "Dedicated compliance support",
                    "SLA guarantees",
                    "On-premise deployment option",
                ]
            }
        ]
    }
