console.log("This is our Soundclub");
let songIndex=0;
let  audioElement = new Audio('1.mp3');
let masterPlay =  document.getElementById('masterPlay');
let ourProgressBar=document.getElementById('ourProgressBar');
let gif =document.getElementById('gif');
let masterSongName  = document.getElementById('masterSongName');
let  songItem=Array.from(document.getElementsByClassName('songItem'));
let  songs =[
    {songName: "TomBoy", filePath: "1.mp3", coversPath: "covers/1.jpg" },
    {songName: "Woman", filePath: "2.mp3", coversPath: "covers/2.jpg" },
    {songName: "Toosie Slide", filePath: "3.mp3", coversPath: "covers/3.jpg" },
    {songName: "Don't Start Now", filePath: "4.mp3", coversPath: "covers/4.jpg" },
    {songName: "Hate Me", filePath: "5.mp3", coversPath: "covers/5.jpg" },
    {songName: "i hate u,i love u", filePath: "6.mp3", coversPath: "covers/6.png" },
    {songName: "Peaches", filePath: "7.mp3", coversPath: "covers/7.png" },
    {songName: "Sad Girlz Luv Money", filePath: "8.mp3", coversPath: "covers/8.png" },
]
songItem.forEach((element,i)=>{
element.getElementsByTagName('img')[0].src = songs[i].coversPath;
element.getElementsByClassName("songName")[0].innerText=songs[i].songName;

})

masterPlay.addEventListener('click',()=>{
if(audioElement.paused || audioElement.currentTime<=0){
    audioElement.play();
    masterPlay.classList.remove('fa-circle-play');
    masterPlay.classList.add('fa-circle-pause');
    gif.style.opacity= 1;
}
else{
    audioElement.pause();
    masterPlay.classList.remove('fa-circle-pause');
    masterPlay.classList.add('fa-circle-play');
    gif.style.opacity= 0;
}
})

audioElement.addEventListener('timeupdate', ()=>{
    console.log('timeupdate');
    progress = parseInt((audioElement.currentTime/audioElement.duration)*100);
    ourProgressBar.value= progress;
})
ourProgressBar.addEventListener('change',()=>{
audioElement.currentTime = ourProgressBar.value * audioElement.duration/100;
})
const  makeAllPlays=()=>{
    
    Array.from(document.getElementsByClassName('songItemPlay')).forEach((element)=>{
    element.classList.remove('fa-circle-pause');
    element.classList.add('fa-circle-play');
})
}

Array.from(document.getElementsByClassName('songItemPlay')).forEach((element)=>{
element.addEventListener('click', (e)=>{
makeAllPlays();
songIndex = parseInt(e.target.id);
e.target.classList.remove('fa-circle-play');
e.target.classList.add('fa-circle-pause');
audioElement.src =`${songIndex+1}.mp3`;
masterSongName.innerText = songs[songIndex].songName;

gif.style.opacity= 1;
audioElement.currentTime=0;
audioElement.play();
    masterPlay.classList.remove('fa-circle-play');
    masterPlay.classList.add('fa-circle-pause');
})
})
document.getElementById('next').addEventListener('click',()=>{
    if(songIndex>=7){
        songIndex=0;
    }
    else{
        songIndex+= 1;
    }   
audioElement.src =`${songIndex+1}.mp3`;
masterSongName.innerText = songs[songIndex].songName;
audioElement.currentTime=0;
audioElement.play();
    masterPlay.classList.remove('fa-circle-play');
    masterPlay.classList.add('fa-circle-pause');
})
document.getElementById('previous').addEventListener('click',()=>{
    if(songIndex<=0){
        songIndex=0;
    }
    else{
        songIndex-= 1;
    }   
audioElement.src =`${songIndex+1}.mp3`;
masterSongName.innerText = songs[songIndex].songName;
audioElement.currentTime=0;
audioElement.play();
    masterPlay.classList.remove('fa-circle-play');
    masterPlay.classList.add('fa-circle-pause');
})

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    document.querySelector("body").classList.add("loaded");
  }, 10)
});
