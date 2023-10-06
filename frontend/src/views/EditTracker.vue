<template>
    <div>
        <div class="card shadow-lg">
            <div class="card-body">
                <h5 class="card-title" style="text-align: center;">
                    {{Title}}
                </h5>
                <a v-if="isEdit" @click="onDelete" class="btn btn-primary">Delete</a>
                <form>
                    <div class="form-group">
                        <label class="card-text">Tracker Name</label><br>
                        <input class="card-textbox" v-model="name" type="text" name="name" requiered />
                    </div>
                    <div class="form-group">
                        <label class="card-text">Description</label><br>
                        <input class="card-textbox" v-model="description" type="text" name="Description" requiered />
                    </div>
                    <div class="form-group">
                        <label class="card-text">Tracker type&nbsp;</label><br>
                        <select class="form-control" v-model="Type">
                            <option value="Numerical" >Numerical</option>
                            <option value="Multiple-choice">Multiple choice</option>
                        </select><br>
                    </div>
                    <div class="form-group">
                        <label class="card-text">Settings</label><br>
                        <input class="card-textbox" v-model="settings" type="text" name="Settings" /><br>
                    </div>
                    <div class="form-group">
                        <label class="card-text">Unit</label><br>
                        <input class="card-textbox" v-model="unit" type="text" name="Units" /><br>
                    </div>
                    <div class="card-text" id="size1">Note: Settings will be ignored if form type Numeric and Unit ignored
                        if Multiple select </div>
                    <input class="btn btn-primary" value="submit" @click='onSubmit'>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    let method='PUT'
    export default {
        name: "EditTracker",
        data: ()=>{
            
            return{
                user: '',
                ID:'',
                name:'',
                description:'',
                Type:'',
                settings:'',
                unit:'',
                Title:'EDIT TRACKER',
                isEdit:true,
                param:''
            }
        },

        methods:
        {
            async onSubmit()
            {   fetch("http://localhost:8800/api/Tracker/"+this.param,
                        {method:method,
                        headers:{'Content-Type':'application/json','Authentication-Token':localStorage.token},
                        body: JSON.stringify(
                           {"Name":this.name,
                            "Description":this.description,
                            "TrackerType":this.Type,
                            "settings":this.settings,
                            "units":this.unit
                        })}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }
                            return res.json()}).then((data)=>{console.log(data)}).catch((err)=>{alert(err)})
                this.$router.push({name: 'dashboard',params: {user:this.user}})
            },
            onDelete()
            {
                fetch("http://localhost:8800/api/Tracker/"+this.ID,
                        {method:'DELETE',headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }else{console.log('DELETED:'+this.ID)}}).catch((err)=>{alert(err)})
                this.$router.push({name: 'dashboard',params: {user:this.user}})
            }
                   
        },
        mounted(){
            this.user=this.$route.params.user
            this.ID=this.$route.params.ID
            this.param=this.ID
            if(this.ID==null){
                method='POST'
                this.Title='CREATE TRACKER'
                this.isEdit=false
                this.param=this.user
            }
            else
            {
                fetch("http://localhost:8800/api/Tracker/"+this.ID,{headers:{"Authentication-Token":localStorage.token}}).then((res)=>{return res.json()})
                .then((data)=>{
                    this.name=data.Name
                    this.description=data.Description
                    this.Type=data.TrackerType
                    this.settings=data.Settings
                    this.unit=data.Units})
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
body
{
    background-color:aquamarine;
}
.btn
{
    color: white;
    margin-bottom: 10px;
}
</style>