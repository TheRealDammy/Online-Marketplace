from typing import Tuple
from PIL import Image


def get_new_image_dimensions(
    original_dimensions: Tuple[int, int], new_width: int
) -> Tuple[int, int]:
    original_width, original_height = original_dimensions

    if original_width < new_width:
        return original_dimensions

    aspect_ratio = original_height / original_width

    new_height = round(new_width * aspect_ratio)

    return (new_width, new_height)


def resize_image(original_image: ImageFieldFile, width: int) -> Image:

    image = Image.open(original_image)

    new_size = get_new_image_dimensions(image.size, width)

    if new_size == image.size:
        return

    return image.resize(new_size, Image.ANTIALIAS)


class ImageWidth:
    THUMBNAIL = 150
    LARGE = 1100


def add_post(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            # form.save() creates a post from the form
            post: Post = form.save(commit=False)

            if post.feature_image:
                img: Image = utils.resize_image(
                    post.feature_image, constants.ImageWidth.LARGE
                )
                img.save(post.feature_image.path)

            post.save()

            return redirect("post_detail", slug=post.slug)

    else:
        form = PostForm()

    context = {"form": form, "edit_mode": False}

    return render(request, "post_form.html", context)
