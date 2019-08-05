index = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="css/custom-style.css">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <title>Manga Viewer</title>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a href="#" class="navbar-brand">MangaK</a>

        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse navbar-toggleable-sm" id="navbarSupportedContent">
            <ul class="navbar-nav">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Manga list
                        <span class="badge badge-light manga-list-len-display"></span>
                    </a>
                    <div class="dropdown-menu manga-list" aria-labelledby="navbarDropdownMenuLink">
                        <a class="dropdown-item" href="#">Action</a>
                        <a class="dropdown-item" href="#">Another action</a>
                        <a class="dropdown-item" href="#">Something else here</a>
                    </div>
                </li>
            </ul>
        </div>
        <div class="btn-group">
            <button type="button" class="btn btn-secondary classic-style">Classic</button>
            <button type="button" class="btn btn-secondary webnovel-style">Webnovel</button>
        </div>
    </nav>

    <div class="jumbotron m-0 p-2 pt-0">
        
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand manga-name-display" href="#">Manga</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse navbar-toggleable-sm" id="navbarNav">
                <div class="dropdown show">
                    <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Chapter list
                        <span class="badge badge-light chapter-list-display"></span>
                    </a>

                    <div class="dropdown-menu chapter-list" aria-labelledby="dropdownMenuLink">
                        <a class="dropdown-item" href="#">Action</a>
                    </div>
                </div>

            </div>
            <ul class="pagination my-auto justify-content-align">
                <li class="page-item"><a class="page-link previous-page" href="#">Previous</a></li>
                <li class="page-item active"><a class="page-link current-page-display" href="#">4</a></li>
                <li class="page-item"><a class="page-link next-page" href="#">Next</a></li>
            </ul>
        </nav>

        <div id="img-container">
        </div>

        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand manga-name-display" href="#">Manga</a>
            <div class="collapse navbar-collapse"></div>
            <ul class="pagination my-auto justify-content-align">
                <li class="page-item"><a class="page-link previous-page" href="#">Previous</a></li>
                <li class="page-item active"><a class="page-link current-page-display" href="#">4</a></li>
                <li class="page-item"><a class="page-link next-page" href="#">Next</a></li>
            </ul>
        </nav>

    </div>

    <footer class="py-2 bg-dark text-white-50">
        <div class="footer-copyright text-center py-3">
            &copy; <script type="text/javascript">
                document.write(new Date().getFullYear())
            </script>
            : <a href="https://github.com/mHaisham">mhaisham@github</a>
        </div>
    </footer>

    <script src="js/jquery-1.12.4.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/script.js"></script>
</body>

</html>"""