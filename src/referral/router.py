from src.register import *
from src.utils.templates import *
from src.client.service import *
from src.auth.v2.auth import *
from src.auth.v2.auth import api_key_header
from src.referral.service import get_referral_subscription_repository, ReferralSubscriptionRepository

router = APIRouter(tags=["Referral(Repository)"])


@router.post("/create/{client_id}", response_model=ReferralSubscriptionReadable)
async def create_client(client_id: int, repository: ReferralSubscriptionRepository = Depends(get_referral_subscription_repository)):
    referral_subscription = await repository.generate_referral_subscription(client_id)
    return referral_subscription
