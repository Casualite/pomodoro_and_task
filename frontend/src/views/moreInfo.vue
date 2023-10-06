<template>
    <div id="parent">
        <b-alert v-model="showDismissibleAlert" variant="warning" dismissible>
      Sending Mail...
    </b-alert>
        <div class="container-fluid">
            <h3 class="title">Tracker View</h3>
            <router-link :to="{name: 'dashboard',params: {user:user}}" class="btn btn-primary" id="dashboard" >Dashboard</router-link>
            <div class="btn-toolbar">
                <a @click='Export' class="btn btn-primary" id="delete">Mail as CSV</a>
                <router-link :to="{name: 'editTracker',params: {user:user,ID:trackerID}}" class="btn btn-primary" id="edit" >Edit</router-link>
                <router-link :to="{name: 'newLog', params: {user:user,ID:trackerID}}" class="btn btn-primary" id="add" >Log</router-link>
                <a @click='onDeleteTracker' class="btn btn-primary" id="delete" >Delete</a>
            </div>
        </div>
        <div id="myChart" v-if="data_x.length"><LineChart :Data_x="data_x" :Data_y="data_y" /></div>
        <div id="table" v-if="data_x.length">
            <table class="table table-dark">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Time</th>
                        <th scope="col">Description</th>
                        <th scope="col">Value</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(x,index) in logs" :key="`x-${index}`">
                        <th scope="row">{{index+1}}</th>
                        <td>{{x.Time}}</td>
                        <td>{{x.note}}</td>
                        <td v-if="flag">{{x.Description}} {{Units}}</td>
                        <td v-else>{{Settings[index-1]}}</td>
                        <td>
                            <router-link :to="{name: 'editLog',params: {user:user,ID:trackerID,Entry:x.EntryNo}}" class="btn btn-primary" id="link" role="button" aria-pressed="true">Edit</router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>  
        <div v-else><h1>Loading or No Values Logged</h1></div>
    </div>
</template>

<script>
    import LineChart from '../components/lineChart.vue'
    export default {
        name:"moreInfo",
        data:()=>{
            return{
                logs:'',
                chartlogs:[],
                plot:false,
                Settings:'',
                trackerID:'',
                user:'',
                flag:true,
                Units:'',
                data_x:[],
                data_y:[],
                showDismissibleAlert:false
            }
        },
        methods:{
            async onDeleteTracker(){
                 await fetch("http://localhost:8800/api/Tracker/"+this.trackerID,
                        {method:'DELETE',headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }else{console.log('DELETED:'+this.ID)}}).catch((err)=>{alert(err)})
                this.$router.push({name: 'dashboard',params: {user:this.user}})
            },
            Export(){
                fetch("http://localhost:8800/make_csv/"+this.user+"/"+this.trackerID).then((res)=>{console.log(res)})
                this.showDismissibleAlert=true
            }
        },
        watch:{chartlogs: function(new_value){
            for (let x in new_value)
            {
                this.data_x.push(this.chartlogs[x].Date)
                this.data_y.push(this.chartlogs[x].Description)
            }}},
        components:{LineChart},
        async mounted(){
            this.trackerID=this.$route.params.ID
            this.user=this.$route.params.user
            let type;
            await fetch("http://localhost:8800/api/Tracker/"+this.trackerID,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    return res.json()
                    }).then((data)=>{
                        type=data.TrackerType
                        if(type!="Numerical")
                        this.flag=false
                        this.Units=data.Units
                        }).catch((error)=>{
                        console.log(error)
                        })
             
             fetch("http://localhost:8800/api/Data/Range/"+this.user+"/"+this.trackerID+"/a",{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    return res.json()
                    }).then((data)=>{
                        this.logs=data
                        }).catch((error)=>{
                            console.log(error)
                        })
             fetch("http://localhost:8800/api/Data/Daily/"+this.user+"/"+this.trackerID+"/a/"+type,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    else
                        this.plot=true
                    return res.json()
                    }).then((data)=>{
                        this.chartlogs=data
                        }).catch((error)=>{
                            console.log(error)
                        })
        }
    }
</script>

<style scoped>
div.container-fluid
{
    height:70px;
    display: flex;
    position: relative;
    background-color: #f3eeaf;
    border-bottom: 5px solid black;
}

body
{
background-color: aquamarine;
}
#dashboard
{
    margin-top: 20px;
    position: absolute;
    color:white
}
.btn-toolbar
{
    margin-top: 20px;
    position: absolute;
    margin-left:80%;
    color:white
    
}
h3.title
{
    position: absolute;
    width:99%;
    text-align: center;
    align-self: center;
}


#table
{
    position:fixed;
    height:400px;
    width:100%;
    overflow: auto;
    bottom:0px;
}

</style>