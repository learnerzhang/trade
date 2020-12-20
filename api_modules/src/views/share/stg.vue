<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="code" label="股票代码" />
    <el-table-column prop="name" label="股票名称" />
    <el-table-column prop="close" label="当前价格" />
    <el-table-column prop="pchg" label="涨幅" />
    <el-table-column prop="high" label="最高价" />
    <el-table-column prop="low" label="最低价" />
    <el-table-column prop="volume" label="成交量" />
    <el-table-column prop="amout" label="成交额" />
  </el-table>
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
