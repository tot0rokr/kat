import vim


def setFileTreeSyntax():
    vim.command("syntax clear")

    # syntax definition
    vim.command("syntax match ftComment /\".*/")


    


    vim.command("hightlight link ftComment Comment")
