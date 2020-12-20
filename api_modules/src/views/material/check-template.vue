<template>
  <div class="root">
    <div class="search">
      <el-input v-model="keyword" placeholder="请输入模板名称" clearable class="input-with-select">
        <el-button slot="append" icon="el-icon-search" @click="goSearch" />
      </el-input>
    </div>
    <el-table
      :data="tableData"
      style="width: 100%"
      :default-sort="{prop: 'createDate', order: 'descending'}"
    >
      <el-table-column prop="name" label="模板名称" show-overflow-tooltip />
      <el-table-column label="上传日期" prop="createDate" sortable>
        <!-- <template slot-scope="scope">{{ scope.row.createDate }}</template> -->
      </el-table-column>
      <el-table-column prop="img_url" label="模板预览">
        <div slot-scope="scope" class="my-pic">
          <el-image
            fit="scale-down"
            style="width: 120px; height: 120px"
            :src="scope.row.imgUrl"
            :preview-src-list="srcList"
            @click="imgClick(scope.row.imgUrl)"
          />
        </div>
      </el-table-column>
      <el-table-column label="操作" align="right">
        <div slot-scope="scope">
          <el-button size="small" type="danger" round @click="deleteTemplate(scope.row.id)">删除</el-button>
          <el-button
            size="small"
            type="primary"
            round
            @click="downloadFile(scope.row.name,scope.row.imgUrl)"
          >下载</el-button>
        </div>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination"
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      @current-change="pageChange"
      @prev-click="pageChange"
      @next-click="pageChange"
    />
    <el-upload
      class="upload template"
      action="http://219.228.76.43:8886/admin/upload"
      :headers="headers"
      :on-success="uploadSuccess"
    >
      <el-button size="small" type="primary">上传模板</el-button>
      <div slot="tip" class="el-upload__tip">只能上传.jpg文件</div>
    </el-upload>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pageSize: 6,
      total: 6, // task总数
      srcList: [],
      tableData: [],
      keyword: "",
      headers: {
        token: localStorage.getItem("token"),
      },
    };
  },
  created: function () {
    this.getTemplateList();
  },
  methods: {
    imgClick(imgUrl) {
      this.srcList = [imgUrl];
    },

    getTemplateList(page = 1, limit = 6) {
      const that = this;
      this.req({
        url: `getTemplateList?page=${page}&limit=${limit}`,
        data: {},
        method: "GET",
      }).then(
        (res) => {
          console.log("res :", res);
          that.total = res.data.total;
          const tableData = res.data.data;
          for (let i = 0; i < tableData.length; i++) {
            tableData[i].createDate = that.getTime(tableData[i].createDate);
          }
          that.tableData = tableData;
        },
        (err) => {
          console.log("err :", err);
        }
      );
    },
    goSearch() {
      const that = this;
      if (that.keyword.length < 1) {
        that.getTemplateList();
        return 0;
      }
      this.req({
        url: "searchTemplate?keyword=" + that.keyword,
        data: {},
        method: "GET",
      }).then(
        (res) => {
          console.log("res :", res);
          if (res.data.length < 1) {
            that.$message("查询无果~");
            return 0;
          } else {
            that.$message("查询成功~");
          }
          for (let i = 0; i < res.data.length; i++) {
            res.data[i].createDate = that.getTime(res.data[i].createDate);
          }
          that.tableData = res.data;
        },
        (err) => {
          console.log("err :", err);
        }
      );
    },
    deleteTemplate(id) {
      const that = this;
      this.$confirm("此操作将删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          that
            .req({
              url: "deleteTemplate?id=" + id,
              data: {},
              method: "GET",
            })
            .then(
              (res) => {
                console.log("res :", res);
                that.getTemplateList();
                that.$message("删除成功~");
              },
              (err) => {
                console.log("err :", err);
              }
            );
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    downloadTemplate(imgUrl) {},
    uploadSuccess(response, file, fileList) {
      const that = this;
      console.log(":", response);
      this.$message("上传成功~");
      this.$prompt("请输入模板名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
      })
        .then(({ value }) => {
          that
            .req({
              url: "addTemplate",
              data: {
                name: value,
                imgUrl: response.data,
                createDate: new Date().getTime(),
              },
              method: "POST",
            })
            .then(
              (res) => {
                console.log("res :", res);
                that.getTemplateList();
              },
              (err) => {
                console.log("err :", err);
              }
            );
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消上传",
          });
        });
    },
    getTime(timestamp) {
      const that = this;
      timestamp = parseInt(timestamp);
      var date = new Date(timestamp); // 时间戳为10位需*1000，时间戳为13位的话不需乘1000
      const Y = date.getFullYear() + "-";
      const M =
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) + "-";
      const D = that.change(date.getDate()) + " ";
      const h = that.change(date.getHours()) + ":";
      const m = that.change(date.getMinutes()) + ":";
      const s = that.change(date.getSeconds());
      return Y + M + D + h + m + s;
    },
    change(t) {
      if (t < 10) {
        return "0" + t;
      } else {
        return t;
      }
    },
    // 下载文件
    downloadFile(name, href) {
      console.log("name :", name);
      console.log("href :", href);
      const a = document.createElement("a"); // 创建a标签
      const e = document.createEvent("MouseEvents"); // 创建鼠标事件对象
      e.initEvent("click", false, false); // 初始化事件对象
      a.href = href; // 设置下载地址
      a.download = name; // 设置下载文件名
      a.dispatchEvent(e); // 给指定的元素，执行事件click事件
    },
    pageChange(page) {
      console.log("page :", page);
      this.getTemplateList(page);
    },
  },
};
</script>

<style>
.upload {
  width: 200px;
  margin: 20px;
  float: right;
}
.my-pic {
  width: 48px;
  height: 27px;
}
.search {
  width: 50%;
  /* margin-left: 50%; */
}
.pagination {
  margin-top: 20px;
  margin-right: 50px;
  float: right;
}
</style>
