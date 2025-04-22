import graphene
from graphene_django import DjangoObjectType
from blogapp.models import Post, Category, Comment, StaticContent
from django.contrib.auth.models import User
from graphql import GraphQLError
from django.db.models import Q

# Type definitions
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'active')

class PostType(DjangoObjectType):
    read_time = graphene.Int()
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'Author', 'image', 'title', 'content', 
                 'category', 'tags', 'status', 'featured', 'trending', 
                 'date', 'views', 'pid')
    
    def resolve_read_time(self, info):
        return self.get_read_time()

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'full_name', 'email', 'comment', 'date', 'active')

class StaticContentType(DjangoObjectType):
    class Meta:
        model = StaticContent
        fields = ('id', 'section_name', 'content')

# Query
class Query(graphene.ObjectType):
    # Post queries
    all_posts = graphene.List(
        PostType,
        search=graphene.String(),
        category=graphene.String(),
        status=graphene.String()
    )
    post = graphene.Field(PostType, pid=graphene.String())
    featured_posts = graphene.List(PostType)
    trending_posts = graphene.List(PostType)
    
    # Category queries
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, slug=graphene.String())
    
    # Comment queries
    post_comments = graphene.List(CommentType, post_id=graphene.String())
    
    # Static content queries
    static_content = graphene.Field(StaticContentType, section_name=graphene.String())

    def resolve_all_posts(self, info, search=None, category=None, status="published"):
        posts = Post.objects.filter(status=status)

        if search:
            filter = (
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(Author__icontains=search)
            )
            posts = posts.filter(filter)

        if category:
            posts = posts.filter(category__slug=category)

        return posts

    def resolve_post(self, info, pid):
        try:
            post = Post.objects.get(pid=pid)
            # Increment views
            post.views += 1
            post.save()
            return post
        except Post.DoesNotExist:
            return None

    def resolve_featured_posts(self, info):
        return Post.objects.filter(featured=True, status="published")

    def resolve_trending_posts(self, info):
        return Post.objects.filter(trending=True, status="published")

    def resolve_all_categories(self, info):
        return Category.objects.filter(active=True)

    def resolve_category(self, info, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    def resolve_post_comments(self, info, post_id):
        return Comment.objects.filter(post__pid=post_id, active=True)

    def resolve_static_content(self, info, section_name):
        try:
            return StaticContent.objects.get(section_name=section_name)
        except StaticContent.DoesNotExist:
            return None

# Mutations
class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.String(required=True)
        full_name = graphene.String(required=True)
        email = graphene.String(required=True)
        comment = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, post_id, full_name, email, comment):
        try:
            post = Post.objects.get(pid=post_id)
            new_comment = Comment.objects.create(
                post=post,
                full_name=full_name,
                email=email,
                comment=comment
            )
            return CreateComment(comment=new_comment)
        except Post.DoesNotExist:
            raise GraphQLError('Post not found!')

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)