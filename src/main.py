from containers import Container


def main():
    container = Container()
    container.wire(modules=["presentation.slack.rag_bot"])

    # VectorStoreの初期化
    vectorstore_tool = container.vectorstore_tool()
    vectorstore_tool.initialize()

    # BackofficeStaffRepositoryの初期化
    backoffice_staff_repository = container.backoffice_staff_repository()
    backoffice_staff_repository.initialize()

    slack_bot = container.slack_bot()
    slack_bot.start()


if __name__ == "__main__":
    main()
