script = """



var MANGA_FOLDER_NAME = 'Manga';
var DATA_FILE_NAME = 'data.json';

// reading styling

var ReadingStyle = {
    CLASSIC: '10px auto',
    WEBNOVEL: '0 auto'
};

function applyStyle(style) {
    $('#img-container img').each(function (index, element) {
        element.style.margin = style;
    });
    setReadingStyle(style);
    switch (style) {
        case ReadingStyle.CLASSIC:
            $('.classic-style').addClass('active');
            $('.webnovel-style').removeClass('active');
            break;
        case ReadingStyle.WEBNOVEL:
            $('.webnovel-style').addClass('active');
            $('.classic-style').removeClass('active');
            break;
    }
}

$('.classic-style').click(function () {
    applyStyle(ReadingStyle.CLASSIC);
});

$('.webnovel-style').click(function () {
    applyStyle(ReadingStyle.WEBNOVEL);
});

// end reading style

// local storage

// set
function setMangaName(value) {
    localStorage.setItem('mname', value);
}

function setChapterList(value) {
    localStorage.setItem('clist', JSON.stringify(value));
}

function setCurrentChapterIndex(value) {
    localStorage.setItem('ccli', value);
}

function setReadingStyle(value) {
    localStorage.setItem('reas', value);
}

// get
function getMangaName() {
    return localStorage.getItem('mname');
}

function getChapterList() {
    return JSON.parse(localStorage.getItem('clist'));
}

function getCurrentChapterIndex() {
    return parseInt(localStorage.getItem('ccli'));
}

function getReadingStyle() {
    return localStorage.getItem('reas');
}

// remove
function removeMangaName() {
    localStorage.removeItem('mname');
}

function removeChapterList() {
    localStorage.removeItem('clist');
}

function removeCurrentChapterIndex() {
    localStorage.removeItem('ccli');
}

// end local storage

// loading

// buttonbindings
$('.previous-page').click(function () { 
    changeChapterBy(-1);
});

$('.next-page').click(function () { 
    changeChapterBy(1);
});


function changeChapterBy(i) {
    setCurrentChapterIndex(Math.max((getCurrentChapterIndex() + i) % Object.keys(getChapterList()).length, 0));
    loadChapterWithIndex(getCurrentChapterIndex());
}

function loadChapterWithIndex(i) {
    loadChapterWithKey(Object.keys(getChapterList())[i]);
}

function loadChapterWithKey(key) {
    loadChapter(key, getChapterList()[key]);
}

function loadChapter(chapter_name, page_list) {
    $('.current-page-display').html(chapter_name);
    $('#img-container').empty();

    setCurrentChapterIndex(Object.keys(getChapterList()).indexOf(chapter_name));
    margin = getReadingStyle();

    $.each(page_list, function(index, value){
        $('<img />')
        .attr('src', '../'+MANGA_FOLDER_NAME+'/'+getMangaName()+'/'+chapter_name+'/'+value)
        .css('margin', margin)
        .appendTo('#img-container');
    });
}

function loadManga(){
    $('.manga-name-display').html(getMangaName());
    $('.current-page-display').html('');
    $('.chapter-list').empty();
    $('#img-container').empty();

    $.getJSON('../'+MANGA_FOLDER_NAME+'/'+getMangaName()+'/tree.json', function(clist){
        // console.log(clist);

        setChapterList(clist);
        $('.chapter-list-display').html(Object.keys(getChapterList()).length);
        $.each(clist, function(key, value){
            
            // create and append element
            $('<a/>')
                .html(key)
                .click(function(){
                    loadChapter(key, value);
                })
                .attr('class', 'dropdown-item')
                .appendTo($('.chapter-list'));
            
        });

    });
    
}

// end loading

// init

function initUnsaved(){
    alert('No saved data');
    removeChapterList();
    removeCurrentChapterIndex();
    removeMangaName();
}

$('.manga-list').empty();
$.getJSON(DATA_FILE_NAME, function(mlist){ // first json
    console.log(mlist);

    $('.manga-list-len-display').html(Object.keys(mlist).length);

    $.each(mlist, function(index, manga){ // first json loop
        // console.log(manga);
        
        $('<a />')
            .html(manga)
            .click(function(){
                setMangaName(manga);
                loadManga(manga);
            })
            .attr('class', 'dropdown-item')
            .appendTo($('.manga-list'));
    });
});

if( getChapterList() == null ||
    getMangaName() == null ||
    getCurrentChapterIndex == null ||
    getCurrentChapterIndex < 0) {
        initUnsaved();
    }
    else{
        loadManga();
        loadChapterWithIndex(getCurrentChapterIndex());
    }

if (getReadingStyle() == null) {
    setReadingStyle(ReadingStyle.CLASSIC);
}else{
    setReadingStyle(getReadingStyle());
}

// end init"""