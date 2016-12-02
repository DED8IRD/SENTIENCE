# These are the controllers for your ajax api.
def get_posts():
    """This controller is used to get the posts.  Follow what we did in lecture 10, to ensure
    that the first time, we get 4 posts max, and each time the "load more" button is pressed,
    we load at most 4 more posts."""
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, orderby=~db.post.created_on, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            p = get_post_output(r)
            posts.append(p)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
    ))


# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_post():
    """Here you get a new post and add it.  Return what you want."""
    p_id = db.post.insert(
        post_content=request.vars.post_content
    )
    p = get_post_output(db.post(p_id))
    return response.json(dict(post=p))


@auth.requires_signature()
def del_post():
    """Used to delete a post."""
    post = db.post[request.vars.post_id]
    if not auth.user or post.user_email != auth.user.email:
        return "no"
    db(db.post.id == request.vars.post_id).delete()
    return "ok"


@auth.requires_signature()
def edit_post():
    """Used to edit a post."""
    post = db.post[request.vars.post_id]
    if not auth.user or post.user_email != auth.user.email:
        return "no"
    db(db.post.id == request.vars.post_id).update(post_content = request.vars.post_content)
    return "{0}{1}".format("Edited On ", post.updated_on)


# Utility functions
def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def get_post_output(post):
    id = post.id
    user_email = post.user_email
    post_content = post.post_content
    user_name = get_user_name_from_email(user_email)
    created_on = post.created_on
    updated = post.created_on != post.updated_on
    updated_on = "" if not updated else "{0}{1}".format("Edited On ", post.updated_on)
    is_mine = auth.user and user_email == auth.user.email
    return dict(
                id=id,
                user_email=user_email,
                post_content=post_content,
                user_name=user_name,
                created_on=created_on,
                updated=updated,
                updated_on=updated_on,
                is_mine=is_mine,
            )
