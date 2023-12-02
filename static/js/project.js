document.getElementById("add_proj").addEventListener("click", hideit);
document.getElementById("undo").addEventListener("click", undo);

function hideit() {

        document.getElementById("add_proj").classList.add("hidden");
        document.getElementById("m_proj")?.classList.add("hidden");
        document.getElementById("o_proj")?.classList.add("hidden");
        document.getElementById("title").classList.add("hidden");
        document.getElementById("form").classList.add("show");
    
    }
    
function undo() {

        document.getElementById("add_proj").classList.remove("hidden");
        document.getElementById("m_proj")?.classList.remove("hidden");
        document.getElementById("o_proj")?.classList.remove("hidden");
        document.getElementById("title").classList.remove("hidden");
        document.getElementById("form").classList.remove("show");
    
    }

function project(){
    let x = document.getElementById("option").value;

        if(x==0){
        document.getElementById("m_proj").style.display = "block";
        document.getElementById("o_proj").style.display = "none";}

        else if(x==1){
            document.getElementById("m_proj").style.display = "none";
            document.getElementById("o_proj").style.display = "block";
        }
        
        else{
            document.getElementById("m_proj").style.display = "block";
            document.getElementById("o_proj").style.display = "block";
        }
    }