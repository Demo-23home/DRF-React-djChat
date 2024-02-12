from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Retrieve a list of servers based on specified filters and parameters.

        Args:
            request (Request): HTTP GET request object.

            category (str, optional): Filter servers by category.
            qty (int, optional): Limit the number of servers returned.
            by_user (bool, optional): Filter servers by the current user.
            by_serverid (int, optional): Filter servers by server ID.
            with_num_members (bool, optional): Include the number of members in the response.

        Raises:
            AuthenticationFailed: If the user is not authenticated and attempts to filter by user or server ID.
            ValidationError: If an invalid server ID is provided or if a server with the given ID doesn't exist.

        Returns:
            Response: Serialized data containing the list of servers.

        Swagger Documentation:
            HTTP Method: GET
            Parameters:
                - category (string, query, optional): Filter servers by category.
                - qty (integer, query, optional): Limit the number of servers returned.
                - by_user (boolean, query, optional): Filter servers by the current user.
                - by_serverid (integer, query, optional): Filter servers by server ID.
                - with_num_members (boolean, query, optional): Include the number of members in the response.
            Response:
                - 200: Serialized data containing the list of servers.
        """
        # Retrieve query parameters
        params = request.query_params
        category = params.get("category")
        qty = params.get("qty")
        by_user = params.get("by_user")
        by_serverid = params.get("by_serverid")
        with_num_members = params.get("with_num_members")

        # Check authentication if needed
        if (by_user or by_serverid) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Annotate queryset with number of members if requested
        if with_num_members == "true":
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Apply filters
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user and request.user.is_authenticated:
            self.queryset = self.queryset.filter(member=request.user.id)

        if by_serverid:
            try:
                server = self.queryset.get(id=by_serverid)
            except Server.DoesNotExist:
                raise ValidationError(
                    {"Details": f"Server with id:{by_serverid} doesn't exist"}
                )
            self.queryset = Server.objects.filter(id=server.id)

        # Slice queryset if quantity is specified
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Serialize queryset with or without number of members based on request
        serializer = ServerSerializer(
            self.queryset,
            many=True,
            context={"num_members": with_num_members == "true"},
        )

        return Response(serializer.data)
