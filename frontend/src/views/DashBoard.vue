<template>
    <div id="exterior">
        
        <div class="container-fluid top h-10">
            <h3 class="title">Dashboard</h3>
            <div class="btn-toolbar" >
                <router-link :to="{name: 'newTracker',params: {user:user}}" id="NewTracker" class="btn btn-primary" @click="newtracker">New Tracker</router-link>
                <router-link :to="{name: 'EditUser',params: {user:user}}" id="edit" class="btn btn-primary" @click="Edit">Edit</router-link>
                <a   class="btn btn-primary" id="log" @click='Logout'>Log Out</a>
            </div>
        </div>
        <div id="trackers">
            <div v-for="(x,index) in trackers"  :key="`x-${index}`">
                <div class="col">
                    <div class="card-body">
                        <div class="card rounded-5 h-100 placeCard">
                            <div class="header"> 
                                <h5 class="card-title">{{x.Name}}</h5>
                            </div>
                            <div>
                                <p class="card-text">
                                Description:{{x.Description}}<br>
                                </p>
                            </div>
                            <div class="card-body" id="links">
                                <router-link :to="{name: 'moreInfo', params: {user:user,ID:x.ID}}" class="card-link">More</router-link>
                                <router-link :to="{name: 'newLog', params: {user:user,ID:x.ID}}" class="card-link">Log</router-link>
                                <router-link :to="{name: 'editTracker',params: {user:user,ID:x.ID}}" @click="Edit" class="card-link">Edit</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default 
    {
        name: "DashBoard",
        data:()=>{return{
            trackers:[],
            user:'',
            
        }},
        methods:{
            async Logout(){
                localStorage.removeItem('token')
                await fetch("/logout")
                this.$router.push({name: 'Login',params: {user:this.user}})
            }
        },
        mounted(){
            this.user=this.$route.params.user
            fetch("http://localhost:8800/api/userTracker/"+this.user, {headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    return res.json()
                    }).then((data)=>{
                        for (let js in data)
                        {   
                            fetch("http://localhost:8800/api/Tracker/"+data[js].ID,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{return res.json()})
                            .then((data)=>{
                                this.trackers.push(data)})
                        }
                        }).catch((error)=>{
                        console.log(error)
                        })
        }
    }
</script>

<style scoped>
body{
    background-color: #f3eeaf;
}
div.container-fluid.top
{
    height:50px;
    display: flex;
    position: absolute;
    border-bottom: 5px solid black;
    background-color: #f3eeaf;
}
#exterior{
    height: 100%;
    margin:0px;
    background-color: #f3eeaf;
}
#links
{
    padding-bottom: 3px;
}

.btn-toolbar
{
    display: inline-block;
    position: absolute;
    background-color: white;
    border-color: black;
    color:white;
    margin-left:80%;
    align-self: center;
}

h3.title
{
    display: inline-block;
    position: absolute;
    width:99%;
    text-align: center;
    align-self: center;
} 
#cards
{
    display: inline-block;
    position:fixed;
} 
#trackers
{
    display: absolute;
    padding-top:40px;
    padding-left:30px;
    padding-right:30px;
    top:50px; 
    margin:0%;
    background-color: #f3eeaf;
}
div.header
{
  text-align: center;
  color: white;
  background-color: rgba(0, 0, 0, 0.842);
  width:100%;
}
</style>