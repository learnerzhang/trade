<template>
  <div style="padding:10px">
    <div style="margin-top: 15px;">
      <div class="search">
        <el-input
          v-model="code"
          placeholder="请输入股票代码(添加交易所前缀,如000001)"
          clearable
          class="input-with-select"
        >
          <el-button slot="append" icon="el-icon-search" @click="goSearch" />
        </el-input>
      </div>
    </div>
    <div class="top">
      <el-row style="margin-left: -5px; margin-right: -5px;">
        <el-col :span="6" style="padding-left: 5px; padding-right: 5px;">
          <el-card>
            <span>{{ name }} ({{ code }})</span>
            <el-divider />
            <div>
              <span>价格</span>
              <el-divider direction="vertical" />
              <span style="font-size: middle;">{{ close }}</span>
              <span style="font-size: small;">({{ date.split(' ')[0] }})</span>
            </div>
            <el-divider />
            <div>
              <span>涨幅</span>
              <el-divider direction="vertical" />
              <span>{{ close - preclose | numFilter }}</span>
              <span v-if="inc">
                <i class="el-icon-top" />
                {{ pctChg | numFilter }}%
              </span>
              <span v-else>
                <i class="el-icon-bottom" />
                {{ pctChg | numFilter }}%
              </span>
            </div>
            <el-divider />
            <div>
              <span>今开</span>
              <el-divider direction="vertical" />
              <span>{{ open }}</span>
            </div>
            <el-divider />
            <div>
              <span>昨收</span>
              <el-divider direction="vertical" />
              <span>{{ preclose }}</span>
            </div>
            <el-divider />
            <div>
              <span>最高</span>
              <el-divider direction="vertical" />
              <span>{{ high }}</span>
            </div>
            <el-divider />
            <div>
              <span>最低</span>
              <el-divider direction="vertical" />
              <span>{{ low }}</span>
            </div>
            <el-divider />
            <div>
              <span>成交量(万手)</span>
              <el-divider direction="vertical" />
              <span>{{ volume }}</span>
            </div>
            <el-divider />
            <div>
              <span>成交额(万)</span>
              <el-divider direction="vertical" />
              <span>{{ amount }}</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="18" style="padding-left: 5px; padding-right: 5px;">
          <el-row>
            <el-tabs v-model="activeTab" style="height: 200px;">
              <el-tab-pane :key="'first'" label="今日分时" name="day" :lazy="true">
                <template>
                  <div>
                    <div ref="chartMin" style="width:540px;height:300px" />
                  </div>
                </template>
              </el-tab-pane>
              <el-tab-pane :key="'second'" label="历史走势" name="history" :lazy="true">
                <template>
                  <div>
                    <div ref="chartHistory" style="width:540px;height:300px" />
                  </div>
                </template>
              </el-tab-pane>
            </el-tabs>
          </el-row>
          <el-row />
          <el-row />
          <el-row />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { getShareTran } from "@/api/trans.js";
import echarts from "echarts";
import VueJsonp from "vue-jsonp";
export default {
  filters: {
    numFilter(value) {
      const realVal = parseFloat(value).toFixed(2);
      return realVal;
    },
  },
  data() {
    return {
      activeTab: "day",
      code: "sh.000001",
      bondCode: "000001",
      type: "sse",
      year: 3,
      name: "上证指数",
      open: 0,
      high: 0,
      low: 0,
      close: 0,
      preclose: 0,
      pctChg: 0,
      amount: 0,
      volume: 0,
      inc: true,
      date: "2020-01-01",
    };
  },
  created: function () {
    console.log("api route => ", this.$route, this.$route.params.code);
    this.code = "sh.000001";
    if (this.$route.params.code != undefined) {
      this.code = this.$route.params.code;
    }
    console.info("api => ", "code:", this.code);
    this.getTran();
    this.$forceUpdate(); // 强行渲染
  },
  mounted: function () {
    window["callback_min"] = (data) => {
      this.callback_min(data);
    };
    // this.getTran()
    // this.$forceUpdate();// 强行渲染
    this.initchart();
    this.getMinChart();
  },
  methods: {
    callback_min: function (data) {
      console.info(data);
    },
    goSearch: function () {
      console.info("api go search: ", this.code);
    },
    getTran: function () {
      getShareTran(this.code).then(
        (res) => {
          console.log("api tran data :", res.data);
          this.code = res.data.code;
          this.name = res.data.name;
          this.amount = res.data.amount;
          this.volume = res.data.volume;
          this.close = res.data.close;
          this.open = res.data.open;
          this.low = res.data.low;
          this.high = res.data.high;
          this.preclose = res.data.preclose;
          this.pctChg = res.data.pctChg;
          this.inc = this.close > this.preclose;
          this.date = res.data.date;
        },
        (err) => {
          console.log("err :", err);
        }
      );
    },
    getMinChart() {
      this.bondCode = this.code.slice(3);
      console.info(this.bondCode);
      if (this.bondCode[0] == 6) {
        this.type = "sse";
      } else {
        this.type = "szse";
      }
      // 第三方接口，需要实时刷新用的定时器，并未做websocket的处理，有需要可以自己加
      // this.timer = setInterval(() => {
      // vue项目中为了规范，跨域请求封装了jsonp的方法
      var min_url =
        "/hexun/a/minute?code=" +
        this.type +
        this.bondCode +
        "&start=20181026000000&number=500&callback=callback_min";
      this.$jsonp(min_url, { fn: "callback_min" })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    initchart() {
      console.info(this.$refs);
      this.chart = echarts.init(this.$refs.chartMin);
    },
  },
};
</script>

<style>
.top {
  padding-top: 50px;
  padding-left: 50px;
}
.el-tabs {
  display: block;
  width: 98%;
}
.el-tabs__item {
  width: 100%;
  text-align: center;
}
</style>
