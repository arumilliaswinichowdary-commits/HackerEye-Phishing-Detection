// ===============================
// HackerEye Professional JS
// ===============================

// Navbar Scroll Effect
window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 60) {

        navbar.style.background = "#06111F";
        navbar.style.padding = "12px 0";
        navbar.style.boxShadow = "0 5px 20px rgba(0,0,0,.4)";

    } else {

        navbar.style.background = "rgba(10,20,35,.75)";
        navbar.style.padding = "18px 0";
        navbar.style.boxShadow = "none";

    }

});


// ===============================
// Smooth Scroll
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        const target=document.querySelector(this.getAttribute("href"));

        if(target){

            target.scrollIntoView({

                behavior:"smooth"

            });

        }

    });

});


// ===============================
// Fade Animation
// ===============================

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("fade-up");

        }

    });

});

document.querySelectorAll(".feature,.card-box,#about,#contact")
.forEach(el=>observer.observe(el));


// ===============================
// Counter Animation
// ===============================

const counters = document.querySelectorAll(".card-box h2");

counters.forEach(counter=>{

    const updateCounter=()=>{

        const text=counter.innerText;

        const target=parseInt(text.replace(/\D/g,''));

        if(isNaN(target)) return;

        let current=0;

        const increment=Math.ceil(target/80);

        const timer=setInterval(()=>{

            current+=increment;

            if(current>=target){

                current=target;

                clearInterval(timer);

            }

            if(text.includes("%")){

                counter.innerText=current+"%";

            }

            else if(text.includes("+")){

                counter.innerText=current+"+";

            }

            else{

                counter.innerText=current;

            }

        },20);

    };

    updateCounter();

});


// ===============================
// Button Ripple Effect
// ===============================

document.querySelectorAll(".btn").forEach(button=>{

    button.addEventListener("click",function(e){

        let circle=document.createElement("span");

        circle.classList.add("ripple");

        this.appendChild(circle);

        const x=e.clientX-this.offsetLeft;

        const y=e.clientY-this.offsetTop;

        circle.style.left=x+"px";

        circle.style.top=y+"px";

        setTimeout(()=>{

            circle.remove();

        },600);

    });

});


// ===============================
// Typing Animation
// ===============================

const heading=document.querySelector(".hero h1");

if(heading){

    const text=heading.innerHTML;

    heading.innerHTML="";

    let i=0;

    function typing(){

        if(i<text.length){

            heading.innerHTML+=text.charAt(i);

            i++;

            setTimeout(typing,25);

        }

    }

    typing();

}


// ===============================
// Floating Animation
// ===============================

setInterval(()=>{

    document.querySelectorAll(".feature").forEach(card=>{

        card.style.transform="translateY(-5px)";

        setTimeout(()=>{

            card.style.transform="translateY(0px)";

        },800);

    });

},4000);


// ===============================
// Loading Effect
// ===============================

window.onload=function(){

    document.body.style.opacity="0";

    setTimeout(()=>{

        document.body.style.transition="1s";

        document.body.style.opacity="1";

    },200);

};


// ===============================
// Hero Button Glow
// ===============================

setInterval(()=>{

    document.querySelectorAll(".btn-primary").forEach(btn=>{

        btn.classList.toggle("glow");

    });

},1200);


// ===============================
// Scroll Progress Bar
// ===============================

const progress=document.createElement("div");

progress.style.position="fixed";
progress.style.top="0";
progress.style.left="0";
progress.style.height="4px";
progress.style.background="#00C3FF";
progress.style.zIndex="99999";

document.body.appendChild(progress);

window.addEventListener("scroll",()=>{

    const scroll=window.scrollY;

    const height=document.documentElement.scrollHeight-window.innerHeight;

    progress.style.width=(scroll/height)*100+"%";

});


// ===============================
// Welcome Console
// ===============================

console.log("================================");

console.log(" HackerEye Professional Edition ");

console.log(" AI Powered Security Platform ");

console.log("================================");