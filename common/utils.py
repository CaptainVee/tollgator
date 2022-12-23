import uuid


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    # usage  = '%s-%s'%('TR',my_random_string(6))
    return random[0:string_length]  # Return the random string.
