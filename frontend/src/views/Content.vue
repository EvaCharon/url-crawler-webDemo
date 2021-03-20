<template>
  <div class="container">
    <div class="leftArea">
      <el-row class="leftTop">
        <el-col :span="24">
          <el-card shadow="never" style="font-size:30px"> {{ `Welcome!   [ ${user} ]` }} </el-card>
        </el-col>
      </el-row>
      <div class="leftBottom">
          <el-card shadow="never"  class="box-card">
            <el-tree 
            node-key="id"
            :data="data" 
            :props="defaultProps" 
            ref="tree"
            show-checkbox
            default-expand-all 
            @node-click="handleNodeClick">
          </el-tree> 
        </el-card>   
      </div>
    </div>
    <div class="rightArea">
      <div class="rightTop">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover" @click.native="scanSelect"> Scan Selected URLs </el-card>
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
            <div class="content">
              <el-card class="box-card">
                  <div v-for="item in working_state"  class="text item" v-bind:key="item.id">
                    {{item }}
                  </div>
                </el-card>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="content">
              <el-card class="box-card">
                  <!-- <div v-for="item in working_state"  class="text item" v-bind:key="item.id">
                    {{item }}
                  </div> -->
                  something to show.
                </el-card>
            </div>
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
        working_state:["No scanning task."],
        expanded_keys: [],
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
      updateURL(){
        this.axios.get("/updateURL").then((response) => {
        console.log(response.data.masterURL);
        let masterURL_array = response.data.masterURL;
        let child_array = response.data.childURL;
        let treeData = new Array();
        for(let i=0;i<masterURL_array.length;i++){
          let ifSelect = false;
          let child = new Array();
          if(i<child_array.length){
            for(let j=0;j<child_array[i].length;j++){
                let empty = new Array();
                let tmp_child = {label:child_array[i][j],children:empty,style:'child',disabled:true};
                child.push(tmp_child);
            }
          }
          let count = new Array();
          if(child.length>0){
            ifSelect = true;
            let empty = new Array();
            let sen  = {label:"  -Total URL:"+String(child.length),children:empty,style:"child",disabled:true};
            count.push(sen);
          } 
          //let tmp = {label:masterURL_array[i],children:child,style:'master',disabled:ifSelect,id:i};
          let tmp = {label:masterURL_array[i],children:count,style:'master',disabled:ifSelect,id:i};
          treeData.push(tmp);
        }
        this.data = treeData;
      })
      },
      scanSelect(){
        console.log(this.$refs.tree.getCheckedKeys());
        let dat = {"index":this.$refs.tree.getCheckedKeys()};
        this.axios.post("/getSelected",dat).then((response) =>{
            console.log(response.data)
        })
      },
      updateState(){
      this.axios.get("/updateState").then((response) => {
        this.working_state.length = 0;
        console.log(this.working_state);
        let sentences = response.data.content;
        this.working_state.push("Press button to start!");
        for(let i=0;i<sentences.length;i++){
            this.working_state.push(String(sentences[i].text));
            //this.working_state+="\n;
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
          let ifSelect = false;
          let child = new Array();
          if(i<child_array.length){
            for(let j=0;j<child_array[i].length;j++){
                let empty = new Array();
                let tmp_child = {label:child_array[i][j],children:empty,style:"child",disabled:true};
                child.push(tmp_child);
            }
          }
          let count = new Array();
          if(child.length>0){
            ifSelect = true;
            let empty = new Array();
            let sen = {label:"  -Total URL:"+String(child.length),children:empty,style:"child",disabled:true};
            count.push(sen);
          }
          //let tmp = {label:masterURL_array[i],children:child,style:'master',disabled:ifSelect,id:i};
          let tmp = {label:masterURL_array[i],children:count,style:'master',disabled:ifSelect,id:i};
          treeData.push(tmp);
        }
        this.data = treeData;
      })
      //this.$options.methods.updateURL();
      //this.updateURL();
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
          let tmp = {label:masterURL_array[i],children:empty,style:"master",id:i};
          treeData.push(tmp);
          this.expanded_keys.push(i);
        }
        this.data = treeData;
        this.updateURL();
        this.updateState();
      })

      // this.axios.get(api).then((response) => {
      //   console.log(response.data)
      // })

      // this.$http.get(api).then((response) => {
      //   console.log(response.data)
      // })
    },
    mounted() {
      this.updateURL();
      this.updateState();
      this.timer = window.setInterval(()=>{
        setTimeout(()=>{
          this.axios.get("/ifUpdate").then((response) => {
          if(response.data.if_updateURL){
              this.updateURL();
          }
          if(response.data.if_updateState){
              this.updateState();
          }      
      }) 
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
    width: 95%;
    height: 95%;
    background: #efefef;
    padding:20px;
    overflow-y:hidden;
    overflow-x:hidden;
  }

  /* 左边 */
  .leftArea {
    width: 25%;
    height: 100%;
    padding-top: 10px;
    display: flex;
    flex-direction: column;
  }

  .leftTop {
    text-align: center;
    height: 10%;
    background-color: #ffffff;
  }

  .leftArea .leftTop .el-card {
    font-weight: 500;
    border: #ffffff;
  }

  .leftBottom {
    width: 100%;
    flex: 1;
    background: #ffffff;
    box-sizing: border-box;
    overflow-y:scroll;
    overflow-x:hidden;
  }

  /* 右边 */
  .rightArea {
    flex: 1;
    height: 100%;
    padding: 10px 20px 10px 20px;
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
    height:80%;
    flex: 1;
    padding-top:15px;
  }
  .rightArea .rightBottom .el-row {
    height: 100%;
  }
  .rightArea .rightBottom .el-row .el-col {
    height: 100%;
  }
  .rightBottom .el-col .content {
    height: 100%;
    padding:10px;
  }
  .rightBottom .el-col .content .box-card{
    overflow-y:scroll;
    overflow-x:hidden;
    height: 95%;
    padding: 10px;
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