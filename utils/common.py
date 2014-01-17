def get_last_rowid(model):
    try:
        return model.objects.latest('pk').pk
    except model.DoesNotExist:
        return 0