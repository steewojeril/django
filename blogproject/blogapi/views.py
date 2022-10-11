from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.models import Mobiles,Carts,Orders
from blogapi.serializers import MobileSerializer,MobileModelSerializer,UserSeializer,ReviewSerializer,CartSerializer,OrderSerializer
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# url:localhost:8000/api/v1/oxygen/mobiles
# get : list all mobiles
# post: create a mobile
class MobilesView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileSerializer(qs,many=True) #ivide cheyyanth deserialize aanu
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=MobileSerializer(data=request.data) #ivide cheyyanth serialize aanu
        if serializer.is_valid(): #validate mtd in serializer class aanu work aavuka
            Mobiles.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
# url:localhost:8000/api/v1/oxygen/mobiles/{id}
# get : list specific data
# put:  to update
# delete: to delete
class MobileDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            qs=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(qs)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"object doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(data=request.data)
            if serializer.is_valid():
                object.name=serializer.validated_data.get("name")
                object.price=serializer.validated_data.get("price")
                object.band=serializer.validated_data.get("band")
                object.display=serializer.validated_data.get("display")
                object.processor=serializer.validated_data.get("processor")
                object.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        except:
            return Response({"msg": "object doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            object.delete()
            return Response({"msg":"deleted"})
        except:
            return Response({"msg": "object doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

# url:localhost:8000/api/v2/oxygen/mobiles
# get : list all mobiles
# post: create a mobile
class MobilesModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# url:localhost:8000/api/v2/oxygen/mobiles/{id}
# get : list specific data
# put:  to update
# delete: to delete
class MobileDetailModelView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(qs)
        return Response(data=serializer.data)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        instance=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Mobiles.objects.get(id=id)
        qs.delete()
        return Response({"msg":"deleted"})

class MobileViewSetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def create(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(object)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Mobiles.objects.get(id=id)
        qs.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)


class MobileModelViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class=MobileModelSerializer
    queryset=Mobiles.objects.all()

# url:localhost:8000/api/v1/oxygen/mobiles/{pid}/add_review/
# post: to add review
# data : review, rating
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# url:localhost:8000/api/v1/oxygen/mobiles/{pid}/get_reviews/
# mtd: to get reviews of specific prooduct
# data : review, rating
    @action(methods=["get"],detail=True)
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        reviews=mobile.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)

    # url:localhost:8000/api/v1/oxygen/mobiles/{pid}/add_to_cart/
    # mtd: post
    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Mobiles.objects.get(id=id)
        user=request.user
        serializer=CartSerializer(data=request.data,context={"product":product,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # url:localhost:8000/api/v1/oxygen/mobiles/{pid}/buy_now/
    # mtd: post
    @action(methods=["post"],detail=True)
    def buy_now(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Mobiles.objects.get(id=id)
        user=request.user
        serializer=OrderSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
# url:localhost:8000/api/v1/oxygen/carts/
    # mtd: get
class CartsView(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset=Carts.objects.all()

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

# url:localhost:8000/api/v1/oxygen/my_orders/
    # mtd: get
class OrdersView(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset=Orders.objects.all()

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSeializer



