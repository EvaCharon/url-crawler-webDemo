<template>
  <div class="container">
    <div class="leftArea">
      <el-row class="leftTop">
        <el-col :span="24">
          <el-card shadow="always"> {{ `Welcome [${user}]` }} </el-card>
        </el-col>
      </el-row>
      <div class="leftBottom">
        <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
      </div>
    </div>
    <div class="rightArea">
      <div class="rightTop">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover"> Scan Selected URLs </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" @click.native="scanAll"> Scan all URLs </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover"> Generate Report </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="rightBottom">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="content">{{`${working_state}`}}</div>
          </el-col>
          <el-col :span="12">
            <div class="content">222</div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        user: window.localStorage.getItem("user"),
        style: {
          borderRadius: "50%",
        },
        working_state:"No scanning task.",
        data: [{
          label: '一级 1',
          children: [{
            label: '二级 1-1',
            children: [{
              label: '三级 1-1-1'
            }]
          }]
        }, {
          label: '一级 2',
          children: [{
            label: '二级 2-1',
            children: [{
              label: '三级 2-1-1'
            }]
          }, {
            label: '二级 2-2',
            children: [{
              label: '三级 2-2-1'
            }]
          }]
        }, {
          label: '一级 3',
          children: [{
            label: '二级 3-1',
            children: [{
              label: '三级 3-1-1'
            }]
          }, {
            label: '二级 3-2',
            children: [{
              label: '三级 3-2-1'
            }]
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      };
    },
    methods: {
      handleNodeClick(data) {
        console.log(data);
      },
      // updateURL(){
      //   this.axios.get("/updateURL").then((response) => {
      //   console.log(response.data.masterURL);
      //   let masterURL_array = response.data.masterURL;
      //   let child_array = response.data.childURL;
      //   let treeData = new Array();
      //   for(let i=0;i<masterURL_array.length;i++){
      //     let child = new Array();
      //     if(i<child_array.length){
      //       for(let j=0;j<child_array[i].length;j++){
      //           let empty = new Array();
      //           let tmp_child = {label:child_array[i][j],children:empty};
      //           child.push(tmp_child);
      //       }
      //     }
      //     let tmp = {label:masterURL_array[i],children:child};
      //     treeData.push(tmp);
      //   }
      //   this.data = treeData;
      // })
      // },
      updateState(){
      this.axios.get("/updateState").then((response) => {
        console.log(this.working_state);
        let sentences = response.data.content;
        this.working_state = "";
        for(let i=0;i<sentences.length;i++){
            this.working_state+=sentences[i].text;
            this.working_state+="\n";
        }
      })
      },
      scanAll(){
        console.log("11")
        this.axios.get("/scanAll").then((response) => {
          console.log(response.data)
        })
        this.axios.get("/updateURL").then((response) => {
        console.log(response.data.masterURL);
        let masterURL_array = response.data.masterURL;
        let child_array = response.data.childURL;
        let treeData = new Array();
        for(let i=0;i<masterURL_array.length;i++){
          let child = new Array();
          if(i<child_array.length){
            for(let j=0;j<child_array[i].length;j++){
                let empty = new Array();
                let tmp_child = {label:child_array[i][j],children:empty};
                child.push(tmp_child);
            }
          }
          let tmp = {label:masterURL_array[i],children:child};
          treeData.push(tmp);
        }
        this.data = treeData;
      })
      //this.$options.methods.updateURL();
      },
     
    },
    beforeCreate() {
      const {
        username
      } = this.$route.params;
      if (username) {
        window.localStorage.setItem("user", username);
      }
      if (!window.localStorage.getItem("user")) {
        this.$message({
          message: "No Login",
          type: "warning",
        });
      }
    },
    created() {
      // 使用方法
      // Vue.axios.get(api).then((response) => {
      //   console.log(response.data)
      // })

      this.axios.get("/getMaster").then((response) => {
        console.log(response.data);
        let masterURL_array = response.data.masterURL;
        let treeData = new Array();
        for(let i=0;i<masterURL_array.length;i++){
          let empty = new Array();
          let tmp = {label:masterURL_array[i],children:empty};
          treeData.push(tmp);
        }
        this.data = treeData;
      })

      // this.axios.get(api).then((response) => {
      //   console.log(response.data)
      // })

      // this.$http.get(api).then((response) => {
      //   console.log(response.data)
      // })
    },
    mounted() {
      this.scanAll();
      this.updateState();
      this.timer = window.setInterval(()=>{
        setTimeout(()=>{
          this.updateState();
        },0)
      },1000)
    },
    components: {},
    destroyed(){
      window.clearINterval(this.timer);
    }
  };
</script>

<style>
  ::-webkit-scrollbar {
    width: 0 !important;
  }

  ::-webkit-scrollbar {
    width: 0 !important;
    height: 0;
  }

  .container {
    display: flex;
    width: 100%;
    height: 100%;
  }

  /* 左边 */
  .leftArea {
    width: 20%;
    height: 100%;
    padding-top: 10px;
    display: flex;
    flex-direction: column;
  }

  .leftTop {
    text-align: center;
    height: 10%;
  }

  .leftArea .leftTop .el-card {
    font-weight: 500;
  }

  .leftBottom {
    width: 100%;
    flex: 1;
    border: 1px solid rgba(0, 0, 0, 0.25);
    box-sizing: border-box;
  }

  /* 右边 */
  .rightArea {
    flex: 1;
    height: 100%;
    padding: 10px 20px 0 20px;
    display: flex;
    flex-direction: column;
  }

  .el-row:last-child {
    margin-bottom: 0;
  }

  .el-col {
    border-radius: 4px;
  }

  .el-button {
    width: 100%;
    height: 100%;
  }

  .rightArea .rightTop {
    width: 100%;
    height: 10%;
  }

  .rightArea .rightBottom {
    width: 100%;
    flex: 1;
  }
  .rightArea .rightBottom .el-row {
    height: 100%;
  }
  .rightArea .rightBottom .el-row .el-col {
    height: 100%;
  }
  .rightBottom .el-col .content {
    border: 1px solid rgba(0, 0, 0, 0.25);
    height: 100%;
  }

  .rightArea .rightTop .el-card {
    border-radius: 40px;
    text-align: center;
    font-weight: 700;
  }

  .rightArea .rightTop .el-card:hover {
    cursor: pointer;
  }
</style>