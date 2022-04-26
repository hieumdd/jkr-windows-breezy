from breezy.pipeline import overview

pipelines = {
    i.name: i
    for i in [
        j.pipeline  # type: ignore
        for j in [
            overview,
        ]
    ]
}
