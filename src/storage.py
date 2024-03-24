import domain
def read():
    d = domain.server(
        type='dns',
        url="1.1.1.1"
    )
    c = domain.server(
        type='dns',
        url="8.8.8.8"
    )

    return domain.appData(
        [
            domain.profile(
                server1 = d,
                server2 = c,
                name = "shekan",
            )
        ]
    )