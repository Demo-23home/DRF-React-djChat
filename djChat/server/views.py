from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        # Retrieve query parameters
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Check if user is authenticated if filtering by user or server id
        if (by_user or by_serverid) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Annotate queryset with number of members if requested
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Filter queryset by category if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter queryset by user if requested
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        # Filter queryset by server id if provided
        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        {"Details": f"Server with id:{by_serverid} doesn't exist"}
                    )
            except ValueError:
                raise ValidationError({"Details": f"Server Value Error"})

        # Slice queryset if quantity is specified
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Serialize queryset with or without number of members based on request
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        return Response(serializer.data)
