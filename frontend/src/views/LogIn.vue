<template>
    <div id="login_form">
        <h5 v-if="register">REGISTER</h5>
        <h5 v-else>LOGIN</h5>
        <b-button v-if="!register" id="register"  @click="register=!register" >register</b-button>
        <b-alert v-if='alert' show variant="danger">Wrong Password</b-alert>
        <b-alert v-if='notExist' show variant="danger">Please Register, user does not exist</b-alert>
        <b-form @submit.prevent>
            <b-form-group v-if="register" id="email" label="email" label-for="email">
                <b-form-input
                id="email"
                v-model="email"
                placeholder="Enter email"
                type="email"
                required
                >
            </b-form-input></b-form-group>
            <b-form-group id="User" label="Username" label-for="Username">
                <b-form-input
                id="Username"
                v-model="Username"
                type="text"
                placeholder="Enter Username"
                required
                ></b-form-input>
            </b-form-group>

            <b-form-group id="pass" label="Password" label-for="password">
                <b-form-input
                id="password"
                v-model="Password"
                placeholder="Enter Password"
                type="password"
                required
                >
            </b-form-input>
            </b-form-group>
            <a v-if="register" id="form_btn" class="btn btn-primary" @click='onRegister' >Register</a>
            <a v-else id="form_btn" class="btn btn-primary" @click='onSubmit' >Submit</a>
            </b-form>
    </div>
    
</template>

<script>
    async function get_token(email,Password)
    {
        let k=true
        console.log('here')
            await fetch("http://127.0.0.1:8800/get_token/login?include_auth_token",{method:'POST',
                            headers:{'Content-Type':'application/json',},
                            body: JSON.stringify({email:email,password:Password})
                            }).then((res)=>{
                    if(!res.ok)
                        throw(res.status+"token not recieved")
                    return res.json()
                }).then((data)=>{localStorage.setItem('token',data.response.user.authentication_token)
                }).catch((error)=>{
                        console.log(error)
                        k=false
                        })
        return(k)
    }
    export default {
        name: "LogIn",
        data: ()=> {
            return{
            Username: '',
            Password: '',
            email:'',
            alert:false,
            register:false,
            notExist:false,
            User_id:0
            }
        },
        methods: {
            async onSubmit()
            {   await fetch("http://localhost:8800/api/login/"+this.Username).then((res)=>{
                    if(!res.ok)
                    {
                        this.notExist=true
                        throw("user does not exist")
                    }
                    return res.json()
                    }
                    ).then((data)=>{
                        this.email=data.email
                        this.User_id=data.id
                }).catch((error)=>{
                        console.log(error)
                        })
                let k=await get_token(this.email,this.Password)
                if(k)
                    this.$router.push({name: 'dashboard',params: {user:this.User_id}})
                else
                    this.alert=true
                
            },
            async onRegister(){
                await fetch("http://localhost:8800/api/login/",
                        {method:'POST',
                        headers:{'Content-Type':'application/json',},
                        body: JSON.stringify({username:this.Username,password:this.Password,email:this.email})
                        }).then((res)=>{return res.json()}).then((data)=>{
                            console.log(data)})
                await fetch("http://localhost:8800/api/login/"+this.Username).then((res)=>{
                    if(!res.ok)
                    throw("user does not exist")
                    return res.json()}).then((data)=>{this.User_id=data.id}).catch((error)=>{
                        console.log(error)
                        })
                let k=await get_token(this.email,this.Password)
                if(k)
                    this.$router.push({name: 'dashboard',params: {user:this.User_id}})

            }
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

</style>