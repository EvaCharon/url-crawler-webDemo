<template>
  <div class="wrapper">
    <el-row type="flex" class="row-bg logo" justify="space-around">
      <el-col :span="6">
        <div class="grid-content bg-purple-light">
          <el-image :src="src" ></el-image>
        </div>
      </el-col>
    </el-row>
    <el-row type="flex" class="row-bg" justify="space-around">
      <el-col :span="6">
        <div class="grid-content bg-purple-light">
          <el-input v-model="username" clearable placeholder="Input Username"></el-input>
        </div>
      </el-col>
    </el-row>
    <el-row type="flex" class="row-bg" justify="space-around">
      <el-col :span="6">
        <div class="grid-content bg-purple-light">
          <el-input type="password" v-model="password" clearable placeholder="Input Password"></el-input>
        </div>
      </el-col>
    </el-row>
    <el-row type="flex" class="row-bg" justify="space-around">
      <el-col :span="6">
        <el-button @click="login">Login</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      src: "https://avatars0.githubusercontent.com/u/74776571?s=100&v=4",
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      const { username, password } = this;
      if(username === "root" && password === "123") {
        this.$message({
          message: "Login Success",
          type: "success"
        });
        this.$router.push({ name: "Content", params: { username } })
      } else if(!username || !password) {
        this.$message({
          message: "The UserName or Password cannot be empty...",
          type: "warning"
        });
      } else {
        this.$message.error("The UserName or Password is incorrect. Please try again");
      }
    },
  },
  components: {},
};
</script>

<style>
.wrapper {
  position: absolute;
  text-align: center;
  width: 100%;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.logo {
  margin-bottom: 10px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
}
.el-input input {
  text-align: center;
}
.el-button {
  width: 60%;
}
</style>
