from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=['guest', 'landlord'], default='guest')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'phone_number', 'role', 'first_name', 'last_name')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    joinedAt = serializers.DateTimeField(source='date_joined', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'role', 'name', 'isActive', 'joinedAt')
        read_only_fields = ('id', 'joinedAt', 'isActive')
    
    def get_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username

class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserSerializer()
    expires_in = serializers.IntegerField()

class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for admin user management - includes all fields and allows updates
    """
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login', 'password'
        )
        read_only_fields = ('id', 'date_joined', 'last_login')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class AdminUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users via admin API
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'is_active', 'is_staff', 
            'is_superuser', 'password', 'password2', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user