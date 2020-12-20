<template>
  <div style="padding:10px">
    <div style="margin-top: 15px;">
      <div class="search">
        <el-input
          v-model="keyword"
          placeholder="请输入股票代码(添加交易所前缀,如sh000001)"
          clearable
          class="input-with-select"
        >
          <el-button slot="append" icon="el-icon-search" @click="goSearch" />
        </el-input>
      </div>
    </div>
    <div class="top" />
  </div>
</template>

<script>
import { getTableData } from "@/api/test.js";
export default {
  data() {
    return {
      tableData: [],
    };
  },
  mounted: function () {
    // 网络请求统一处理
    getTableData().then(
      (res) => {
        console.log("api share tableData :", res);
        this.tableData = res.data;
      },
      (err) => {
        console.log("err :", err);
      }
    );
    // 网络请求直接写在文件中
    // this.req({
    //   url: "getTableData",
    //   data: {},
    //   method: "GET"
    // }).then(
    //   res => {
    //     console.log("tableData :", res);
    //     this.tableData = res.data;
    //   },
    //   err => {
    //     console.log("err :", err);
    //   }
    // );
  },
  methods: {},
};
</script>

<style>
</style>
