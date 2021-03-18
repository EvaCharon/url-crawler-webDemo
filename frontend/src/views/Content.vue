<template>
  <div class="container">
    <div class="leftArea">
      <el-row class="leftTop">
        <el-col :span="24">
          <el-card shadow="always"> {{ `Welcome [${user}]` }} </el-card>
        </el-col>
      </el-row>
      <div class="leftBottom"></div>
    </div>
    <div class="rightArea">
      <div class="rightTop">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover"> xxxxx </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover"> Scan all </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover"> Generate Report </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="rightBottom">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="content">11111</div>
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
      };
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
    mounted() {},
    components: {},
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