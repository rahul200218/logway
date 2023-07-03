var counter=1;
setInterval(function(){
    document.getElementById('radio'+ counter).checked=true;
    counter++;
    if (counter>4){
        counter=1;
    }
},5000);



document.getElementById("divicon").addEventListener('click',displaymenu);
function displaymenu()
{
    var a=document.getElementsByClassName('menu');
    a[0].style.height = "150px";
    a[0].style.boxShadow="rgba(0,0,0,0.45) 25px 25px 25px 25px";

}

document.getElementById("close").addEventListener('click',closemenu);
function closemenu()
{
    var a=document.getElementsByClassName('menu');
    a[0].style.height = "0px";
    a[0].style.boxShadow="rgba(0,0,0,0.45) 0px 0px 0px 0px";
}


// document.getElementById("dark").addEventListener("click",darkmode);
// function darkmode()
// {
//     let a=document.getElementById("light");
//     a.classList.add("vis");
//     let b=document.getElementById("dark");
//     b.classList.add("disp");

// }

// document.getElementById("light").addEventListener("click",lightmode);
// function lightmode()
// {
//     let a=document.getElementById("dark");
//     a.classList.add("vis");
//     let b=document.getElementById("light");
//     b.classList.add("disp");

// }


let sect=document.querySelectorAll('section ');
let navlink=document.querySelectorAll('header a');
window.onscroll=()=>
{
    sect.forEach(sec =>
        {
            let top=window.scrollY;
            let offset=sect.offsetTop;
            let height=sect.offsetHeight;
            let id=sect.getAttribute('id');
            

        })
}

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
    } else {
      entry.target.classList.remove('is-visible');
    }
    });
    });
    
    document.querySelectorAll('.box').forEach(box => {
    observer.observe(box);
    });

var bar=document.getElementById("menu-bar");
var smart=document.getElementById("smart-div-div");
var list2=document.getElementById("list1");
bar.addEventListener("click",myfun3);
function myfun3()
{
    smart.style.visibility="visible";
   
   
    smart.style.opacity="1";
    list2.style.opacity="1";
    
}

var xmark=document.getElementById("xmark")
var smart=document.getElementById("smart-div-div");
xmark.addEventListener("click",myfun4);
function myfun4()
{
    smart.style.visibility="hidden";
   
   
}


let section=document.querySelectorAll('section');
let navlinks=document.querySelectorAll(' list-link a');
window.onscroll=()=>{
    section.forEach(sec =>{
        let top=window.scrollY;
        let offset=sec.offsetTop - 150;
        let height=sec.offsetHeight;
        let id=sec.getAttribute('id');

        if(top >= offset &&  top < offset + height){
            navlinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('list-link a[href "=" + id +]').classList.add("active");
            })
        }
    })
}