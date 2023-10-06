<template>
    <div id="login_form">
        <a @click="onDelete" class="btn btn-primary">Delete</a>
        <h5>Edit account</h5>
        <b-alert v-if='alert' show variant="danger">Wrong Password</b-alert>
        <b-form @submit.prevent>
            <b-form-group id="pass" label="Password" label-for="password">
                <b-form-input
                id="password"
                v-model="Password"
                placeholder="Enter New Password"
                type="password"
                required
                >
            </b-form-input>
            </b-form-group>
            <b-button id="form_btn" type="submit" variant="primary" @click='onSubmit' >Submit</b-button>
            </b-form>
    </div>
    
</template>

<script>
    export default {
        name: "editUser",
        data: ()=> {
            return{
            Username: '',
            Password: '',
            alert:false,
            }
        },
        methods: {
            onSubmit()
            {   
                fetch("http://localhost:8800/api/login/"+this.Username,
                        {method:'PUT',
                        headers:{'Content-Type':'application/json',"Authentication-Token":localStorage.token},
                        body: JSON.stringify({password:this.Password,active:true})
                        }).then((res)=>{return res.json()}).then((data)=>{console.log(data)})
                this.$router.push({name: 'Login'})//cause token changes
            },
            onDelete(){
               fetch("http://localhost:8800/api/login/"+this.Username,
                        {method:'DELETE',headers:{"Authentication-Token":localStorage.token}}).then((res)=>{
                            if(!res.ok)
                            {
                                throw("status code: "+res.status)
                            }else{console.log('DELETED:'+this.Username)}}).catch((err)=>{alert(err)}) 
                this.$router.push({name: 'Login'})
            }
        },
        mounted()
        {
            this.Username=this.$route.params.user
        }
        
    }
</script>

<style scoped>
#login_form
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
#login_form>h5{
    color:Black;
}
#exterior
{
    color: #f3eeaf;
}
#form_btn
{
    margin-top: 20px;
}
.btn
{
    color: white;
    margin-bottom: 10px;
}
</style>