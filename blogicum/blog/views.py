from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic import DeleteView
from .models import Category, Post, User, Comment
from .constants import TOTAL_POSTS
from .forms import PostForm, CommentForm
from .mixins import AuthorMixin, CommentMixin, PostMixin
from .utils import filter_search, filter_search_comment


class CategoryDetailView(ListView):
    template_name = 'blog/category.html'
    paginate_by = TOTAL_POSTS
    slug_url_kwarg = 'category_slug'

    def get_category(self):
        return get_object_or_404(
            Category, slug=self.kwargs[self.slug_url_kwarg], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_queryset(self):
        return filter_search(filter_search_comment(self.get_category().posts))


class PostListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = TOTAL_POSTS
    queryset = filter_search_comment(filter_search(Post.objects))


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    paginate_by = TOTAL_POSTS

    def get_object(self) -> Model:
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if self.request.user == post.author:
            return post
        return get_object_or_404(filter_search(Post.objects),
                                 id=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = post.comments.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostDeleteView(PostMixin, AuthorMixin, DeleteView):
    pass


class PostUpdateView(PostMixin, AuthorMixin, UpdateView):
    pass


class CommentCreateView(CommentMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(filter_search(
            Post.objects),
            pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CommentUpdateView(CommentMixin, AuthorMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, AuthorMixin, DeleteView):
    pass


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = TOTAL_POSTS

    def get_profile(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        author = self.get_profile()
        posts = filter_search_comment(author.posts)
        if author == self.request.user:
            return posts
        return filter_search(posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'username', 'email')
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.kwargs[self.slug_url_kwarg]})
