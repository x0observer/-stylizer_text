from src.register import *
from src.utils.templates import *
from src.client.service import *
from src.auth.v2.auth import *
from src.auth.v2.auth import api_key_header
from src.referral.service import get_referral_subscription_repository, ReferralSubscriptionRepository

router = APIRouter(tags=["Referral(Repository)"])


@router.post("/create/{client_id}", response_model=ReferralSubscriptionReadable)
async def create_referral_subscription(client_id: int, repository: ReferralSubscriptionRepository = Depends(get_referral_subscription_repository)):
    referral_subscription = await repository.generate_referral_subscription(client_id)
    return referral_subscription


@router.get("/get/{code}", response_model=ReferralSubscriptionReadable)
async def get_client_from_referral_subscription(code: str, repository: ReferralSubscriptionRepository = Depends(get_referral_subscription_repository)):
    referral_subscription = await repository.get_client(code)
    return referral_subscription


@router.post("/attach/")
async def attach_client_to_referral_subscription(code: str, client_id: int, repository: ReferralSubscriptionRepository = Depends(get_referral_subscription_repository)):
    referral_bundle = await repository.attach_clinet(code, client_id)
    return referral_bundle
