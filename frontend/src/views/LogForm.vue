<template>
    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title" style="text-align: center;">
                {{Title}}
            </h5>
            <form>
                <a v-if="toEdit" @click="onDelete" class="btn btn-primary">Delete</a>
                <div v-if="toEdit" class="form-group">
                    <label class="card-text">Log Date</label>
                    <input class="card-textbox" v-model="date" type="datetime-local" />
                </div>
                <div v-if="Numeric" class="form-group">
                    <label class="card-text">Enter value</label>
                    <input class="card-textbox" type="number" v-model="value" requiered />
                </div>
                <div v-else class="form-group">
                    <label class="card-text">Setting&nbsp;</label>
                    <select class="form-control" v-model="value">
                        <option v-for="(x,index) in settings" :key="`x-${index}`"  :value="x">{{x}}</option>
                    </select><br>
                </div>
                <div class="form-group">
                    <label class="card-text">Note</label>
                    <input class="card-textbox" type="text" v-model="note" />
                </div>
                <a v-if="toEdit" class="btn btn-primary"  @click='onUpdate'>Update</a>
                <a v-else class="btn btn-primary" @click='onSubmit'>Submit</a>
            </form>
        </div>
    </div>
</template>

<script>
    export default {
        name:"logForm",
        data:()=>{
            return{
            value:'',
            note:'',
            date:'',
            Numeric:'',
            settings:[],
            Title:'',
            ID:'',
            Entry:'',
            user:'',
            }
        },
        props:{
            toEdit:Boolean
        },
        methods:{
            async onSubmit()
            {
                let k=0
                console.log("onSubmit")
                if(this.Numeric)
                    k=parseInt(this.value)
                else
                    k=this.settings.indexOf(this.value)
                await fetch("http://localhost:8800/api/Data/"+this.user+"/"+this.ID,
                        {method:"POST",
                        headers:{'Content-Type':'application/json',"Authentication-Token":localStorage.token},
                        body: JSON.stringify(
                           {"Description":k,
                            "note":this.note}
                            )}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }
                            return res.json()}).then((data)=>{console.log(data)}).catch((err)=>{alert(err)})
                this.$router.push({name: 'moreInfo',params: {user:this.user,ID:this.ID}})
            },
            async onUpdate()
            {   
                console.log("onUpdate")
                let k=0
                if(this.date.length==0)
                this.date=false
                if(this.Numeric)
                    k=parseInt(this.value)
                else
                    k=this.settings.indexOf(this.value)
                await fetch("http://localhost:8800/api/Data/"+this.user+"/"+this.ID+"/"+this.Entry,
                        {method:"PUT",
                        headers:{'Content-Type':'application/json','Authentication-Token':localStorage.token},
                        body: JSON.stringify(
                           {"Description":k,
                            "note":this.note,
                            "Time":this.date}
                            )}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }
                            return res.json()}).then((data)=>{console.log(data)}).catch((err)=>{alert(err)})
                this.$router.push({name: 'moreInfo',params: {user:this.user,ID:this.ID}})
            },
            onDelete()
            {
                fetch("http://localhost:8800/api/Data/"+this.Entry,
                        {method:'DELETE',headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }else{console.log('DELETED:'+this.Entry)}}).catch((err)=>{alert(err)}) 
                this.$router.push({name: 'moreInfo',params: {user:this.User_id,ID:this.ID}})
            }
        },
        mounted(){
            this.ID=this.$route.params.ID
            this.user=this.$route.params.user
            this.Title="New Log"
            fetch("http://localhost:8800/api/Tracker/"+this.ID,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    return res.json()
                    }).then((data)=>{
                        this.Numeric=false
                        if(data.TrackerType=="Numerical")
                            this.Numeric=true
                        else
                            this.settings=data.Settings.split(",")
                        }).catch((error)=>{
                        console.log(error)
                        })
            if(this.toEdit){
                this.Entry=parseInt(this.$route.params.Entry)
                this.Title="Update Log"
                fetch("http://localhost:8800/api/Data/"+this.Entry,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                    if(!res.ok)
                    {
                        throw(res.status)
                    }
                    return res.json()
                    }).then((data)=>{
                        this.value=data.Description
                        if(!this.Numeric)
                            this.value=this.settings[this.value]
                        this.note=data.note
                        }).catch((error)=>{
                        console.log(error)
                        })
            }
        }
    }
</script>

<style scoped>
.card
{
  margin:auto;
  border-radius: 15px;
  background: #f3eeaf;
  padding: 20px;
  width: fit-content;
  height: fit-content;
  position:absolute;
  top:0; left:0; right:0; bottom:0; 
}
.card>h5{
    color:Black;
}
</style>