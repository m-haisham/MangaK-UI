style = '''

:root {
    --main-fore-color: #039be5;
    --main-bg-color: #2d3436;
}

body {
    margin: 0;
    padding: 0;
    background: var(--main-bg-color);
    font: 15px Arial, Helvetica, sans-serif;
}

a {
    text-decoration: none;
}

ul {
    list-style: none;
    padding-left: 0;
}

.container {
    width: 100%;
    margin: auto;
    overflow: hidden;
}

.manga {
    text-align: center;
}

.chapter-bar {
    display: flex;
    margin: 10px auto;
    justify-content: center;
    align-items: center;
}

.chapter-title {
    font-size: 18px;
    color: var(--main-fore-color);
    padding: 7px 20px;
    border: 2px solid var(--main-fore-color);
    border-radius: 5px;
    text-decoration: none;
}

.title-container {
    display: flex;
    margin: 10px auto;
    justify-content: center;
    align-items: center;
}

.manga-title {
    font-size: 22px;
    color: var(--main-fore-color);
    border: 2px solid var(--main-fore-color);
    border-radius: 5px;
    text-transform: capitalize;
    text-align: center;
    margin: 20px auto 0 auto;
    padding: 10px 30px;
}

.title {
    transition: .2s;
}

.title:hover {
    background-color: var(--main-fore-color);
    color: var(--main-bg-color);
}

.btn {
    border: none;
    font-family: inherit;
    font-size: inherit;
    color: inherit;
    background: none;
    cursor: pointer;
    padding: 9px 20px;
    min-width: 100px;
    display: inline-block;
    margin: 5px 10px;
    text-transform: uppercase;
    text-decoration: none;
    text-align: center;
    letter-spacing: 1px;
    font-weight: 600;
    outline: none;
    position: relative;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
}

.btn:after {
    content: '';
    position: absolute;
    z-index: -1;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
}

/* Button 1 */
.btn-1 {
    border: 2px solid var(--main-fore-color);
    color: var(--main-fore-color);
}

.btn-left {
    border-radius: 30px 5px 5px 30px;
}

.btn-right {
    border-radius: 5px 30px 30px 5px;
}

/* Button 1d */
.btn-1d {
    overflow: hidden;
}

.btn-1d:after {
    width: 0;
    height: 103%;
    top: 50%;
    left: 50%;
    background: var(--main-fore-color);
    opacity: 0;
    -webkit-transform: translateX(-50%) translateY(-50%);
    -moz-transform: translateX(-50%) translateY(-50%);
    -ms-transform: translateX(-50%) translateY(-50%);
    transform: translateX(-50%) translateY(-50%);
}

.btn-1d:hover,
.btn-1d:active {
    color: var(--main-bg-color);
}

.btn-1d:hover:after {
    width: 90%;
    opacity: 1;
}

.btn-1d:active:after {
    width: 101%;
    opacity: 1;
}

.page {
    max-width: 100%;
    display: block;
    margin: 0 auto 5px;
    z-index: 1!important;
}'''