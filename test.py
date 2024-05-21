class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
        )
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "이메일을 입력해주세요.",
                    "invalid": "알맞은 형식의 이메일을 입력해주세요.",
                    "blank": "이메일을 입력해주세요.",
                }
            },
            "phone_number": {
                "error_messages": {
                    "required": "휴대폰 번호를 입력해주세요.",
                }
            },
        }

    def validate(self, data):
        phone_number = data.get("phone_number")
        current_phone_number = self.context.get("request").user.phone_number

        # 휴대폰 번호 존재여부와 blank 허용
        if User.objects.filter(phone_number=phone_number).exclude(phone_number=current_phone_number).exists() and not phone_number == "":
            raise serializers.ValidationError(detail={"phone_number": "이미 사용중인 휴대폰 번호 이거나 탈퇴한 휴대폰 번호입니다."})

        return data

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.save()

        return instance


# 비밀번호 변경 serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        error_messages={
            "required": "비밀번호를 입력해주세요.",
            "blank": "비밀번호를 입력해주세요.",
            "write_only": True,
        }
    )
    repassword = serializers.CharField(
        error_messages={
            "required": "비밀번호를 입력해주세요.",
            "blank": "비밀번호를 입력해주세요.",
            "write_only": True,
        }
    )

    class Meta:
        model = User
        fields = (
            "password",
            "repassword",
            "confirm_password",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호를 입력해주세요.",
                    "blank": "비밀번호를 입력해주세요.",
                },
            },
        }

    def validate(self, data):
        current_password = self.context.get("request").user.password
        confirm_password = data.get("confirm_password")
        password = data.get("password")
        repassword = data.get("repassword")

        # 현재 비밀번호 예외 처리
        if not check_password(confirm_password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 비밀번호가 일치하지 않습니다."})

        # 현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."})

        # 비밀번호 일치
        if password != repassword:
            raise serializers.ValidationError(detail={"password": "비밀번호가 일치하지 않습니다."})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(
                detail={"password": "비밀번호는 8자 이상 16자이하의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다. "}
            )

        # 비밀번호 문자열 동일여부 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 3자리 이상 동일한 영문/사용 사용 불가합니다. "})

        return data

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()

        return instance
