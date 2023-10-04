from django.contrib.auth.models import AbstractUser

# from django.contrib.gis.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True)
    profile_message = models.CharField(max_length=200, blank=True, default="")  # type: ignore

    library_latitude = models.FloatField(null=True)  # type: ignore # 위도
    library_longitude = models.FloatField(null=True)  # type: ignore # 경도


#  source 유저가 target 유저를 팔로우한다.
#  source 유저는 FR과 1대1 관계이고, FR과 target 유저는 M대N관계읻.
class FollowingRelation(models.Model):
    source_user_id = models.OneToOneField(  # type: ignore
        to="User",  #  객체를 직접 매핑하지 않고 문자열로 매핑 -> 순환참조 방지
        on_delete=models.CASCADE,
    )
    target_user_id = models.ManyToManyField(  # type: ignore
        to="User",
        null=False,
        on_delete=models.CASCADE,
    )
    # class Meta:
    #     constraints = (
    #         models.CheckConstraint(
    #             check=models.Q(source_user_id != target_user_id)
    #         )
    #     )
