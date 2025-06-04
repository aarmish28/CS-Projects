const main_video = document.querySelector('.main-video video');
const main_video_title = document.querySelector('.main-video .title');
const video_playlist = document.querySelector('.video-playlist .videos');

let data = [
    {
        'id': 'a1',
        'title': 'Mocking Bird',
        'name': '8.mp4',
        'duration': '04:17',
    },
    {
        'id': 'a2',
        'title': 'Break My Heart Myself',
        'name': '2.mp4',
        'duration': '02:33',
    },
    {
        'id': 'a3',
        'title': 'I Like Me Better',
        'name': '3.mp4',
        'duration': '03:20',
    },

    {
        'id': 'a4',
        'title': 'Starboy',
        'name': '4.mp4',
        'duration': '04:33',
    },
    {
        'id': 'a5',
        'title': "Princesses Don't Cry",
        'name': '5.mp4',
        'duration': '04:30',
    },
    {
        'id': 'a6',
        'title': 'Blinding Lights',
        'name': '6.mp4',
        'duration': '04:22',
    },
    {
        'id': 'a7',
        'title': 'No Lie',
        'name': '7.mp4',
        'duration': '03:48',
    },
    {
        'id': 'a8',
        'title': 'Money',
        'name': '1.mp4',
        'duration': '02:50',
    },
];

data.forEach((video, i) => {
    let video_element = `
                <div class="video" data-id="${video.id}">
                    <img src="images/play.svg" alt="">
                    <p>${i + 1 > 9 ? i + 1 : '0' + (i + 1)}. </p>
                    <h3 class="title">${video.title}</h3>
                    <p class="time">${video.duration}</p>
                </div>
    `;
    video_playlist.innerHTML += video_element;
})

let videos = document.querySelectorAll('.video');
videos[0].classList.add('active');
videos[0].querySelector('img').src = 'images/pause.svg';


videos.forEach(selected_video => {
    selected_video.onclick = () => {

        for (all_videos of videos) {
            all_videos.classList.remove('active');
            all_videos.querySelector('img').src = 'images/play.svg';

        }

        selected_video.classList.add('active');
        selected_video.querySelector('img').src = 'images/pause.svg';

        let match_video = data.find(video => video.id == selected_video.dataset.id);
        main_video.src = 'videos/' + match_video.name;
        main_video_title.innerHTML = match_video.title;
    }
});
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      document.querySelector("body").classList.add("loaded");
    }, 10)
  });
  
