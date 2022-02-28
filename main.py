if __name__ == "__main__":
    import pirategame
    app = pirategame.App()
    print(app.client.user)
    app.start_client()