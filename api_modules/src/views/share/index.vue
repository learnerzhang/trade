<template>
  <div class="root">
    <form class="el-form demo-form-inline el-form--inline">
      <div class="el-form-item">
        <label class="el-form-item__label">股票名称</label>
        <div class="el-form-item__content">
          <el-input
            v-model="keywords"
            type="text"
            placeholder="股票名称"
            style="width: 200px;"
            class="filter-item"
            @input="input_change($event)"
          />
        </div>
      </div>
      <div class="el-form-item">
        <label class="el-form-item__label">板块行业</label>
        <el-select v-model="industryValue" placeholder="全部行业" @change="changeIndustry">
          <el-option
            v-for="item in industryGroup"
            :key="item.id"
            :label="item.value"
            :value="item.value"
          />
        </el-select>
      </div>
      <div class="el-form-item">
        <!---->
        <div class="el-form-item__content">
          <el-button class="filter-item" type="primary" icon="el-icon-search" @click="onSearch">
            <span>查询</span>
          </el-button>
        </div>
      </div>
    </form>

    <el-table
      v-loading="loading"
      :data="shareData"
      border
      stripe
      style="width: 100%"
      :default-sort="{prop: 'code', order: 'ascending'}"
      @sort-change="changeSort"
      @row-click="clickTbRow"
    >
      <el-table-column fixed prop="code" label="股票代码" />
      <el-table-column prop="name" label="股票名称" />
      <el-table-column sortable="custom" prop="close" label="当前价格" />
      <el-table-column sortable="custom" prop="pctChg" label="涨幅" />
      <el-table-column sortable="custom" prop="high" label="最高价" />
      <el-table-column sortable="custom" prop="low" label="最低价" />
      <el-table-column sortable="custom" prop="volume" label="成交量(万)" />
      <el-table-column sortable="custom" prop="amount" label="成交额(万)" />
    </el-table>
    <div class="pagination">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[5, 10, 20, 40]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next"
        :total="totalnum"
        prev-text="上一页"
        next-text="下一页"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { getTransData } from "@/api/trans.js";
import { getIndustryData } from "@/api/share.js";
export default {
  data() {
    return {
      currentPage: 1, // 默认显示页面为1
      pagesize: 10, // 每页的数据条数
      tableData: [],
      loading: true,
      totalnum: 0,
      sortorder: 1,
      sortfield: "code",
      keywords: "",
      industryValue: null,
      industryGroup: [],
      shareData: [],
    };
  },
  created: function () {
    // this.getTableData();
    // this.getIndustryGroup();
  },
  mounted: function () {
    this.getTableData();
    this.getIndustryGroup();
  },
  methods: {
    clickTbRow: function (row) {
      console.info("api click jump :", row.code);
      this.$router.push({ path: "/share/detail/" + row.code });
    },
    onSearch: function () {
      console.info("api search:", this.keyword, this.industryValue);
      // 网络请求统一处理
      console.info(
        "api request => page:" +
          this.currentPage +
          ", size:" +
          this.pagesize +
          ", field:" +
          this.sortfield +
          ", order:" +
          this.sortorder +
          ", keyword:" +
          this.keywords +
          ", industry:" +
          this.industryValue
      );
      getTransData(
        0,
        this.pagesize,
        this.sortfield,
        this.sortorder,
        this.keywords,
        this.industryValue
      ).then(
        (res) => {
          console.log("api trans tableData :", res);
          this.shareData = res.data;
          this.pagesize = res.pagesize;
          this.currentPage = res.page;
          this.totalPages = res.totalPages;
          this.totalnum = res.totalnum;
          this.loading = false;
          this.$forceUpdate(); // 强行渲染
        },
        (err) => {
          console.log("err :", err);
        }
      );
    },
    changeIndustry: function (data) {
      console.info("api change:", data);
      this.$forceUpdate();
    },
    input_change: function (e) {
      this.$forceUpdate();
    },
    handleSizeChange: function (size) {
      this.pagesize = size;
      this.getTableData();
      // console.log("改变页面大小:" + this.pagesize)
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      this.getTableData();
      // console.log("跳转页:" + this.currentPage)
    },
    changeSort: function (val) {
      // console.log(val) // column: {…} order: "ascending" prop: "date"
      if (val.column) {
        this.sortfield = val.prop;
        if (val.order == "ascending") {
          // 升序
          this.sortorder = 1;
        } else if (val.order == "descending") {
          // 降序
          this.sortorder = -1;
        } else {
          // 默认code排序
          this.sortorder = 1;
          this.sortfield = "code";
        }
        this.getTableData();
      }
    },
    getTableData: function () {
      // 网络请求统一处理
      console.info(
        "api request => page:" +
          this.currentPage +
          ", size:" +
          this.pagesize +
          ", field:" +
          this.sortfield +
          ", order:" +
          this.sortorder +
          ", keyword:" +
          this.keywords +
          ", industry:" +
          this.industryValue
      );
      getTransData(
        this.currentPage,
        this.pagesize,
        this.sortfield,
        this.sortorder,
        this.keywords,
        this.industryValue
      ).then(
        (res) => {
          console.log("api trans tableData :", res);
          this.shareData = res.data;
          this.pagesize = res.pagesize;
          this.currentPage = res.page;
          this.totalPages = res.totalPages;
          this.totalnum = res.totalnum;
          this.loading = false;
          this.$forceUpdate(); // 强行渲染
        },
        (err) => {
          console.log("err :", err);
        }
      );
      // 网络请求直接写在文件中
      // this.req({
      //   url: "/tran/daily_trans",
      //   data: {},
      //   method: "POST"
      // }).then(
      //   res => {
      //     console.log("tableData :", res);
      //     this.tableData = res.data;
      //     this.pageSize = res.pageSize;
      //   },
      //   err => {
      //     console.log("err :", err);
      //   }
      // );
    },
    getIndustryGroup: function () {
      getIndustryData().then(
        (res) => {
          console.log("api industry tableData :", res);
          res.data.forEach((item) => {
            this.industryGroup.push(item);
          });
          // for(var i = 0; i < res.data.length; i++){
          //     this.industryGroup.push((i, res.data[i]))
          // }
          this.$forceUpdate(); // 强行渲染
        },
        (err) => {
          console.log("err :", err);
        }
      );
    },
  },
};
</script>

<style>
</style>
