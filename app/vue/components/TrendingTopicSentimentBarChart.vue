<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <div :id="sentimentGraphId" v-bind="attrs"
        v-on="on">
    </div>
    </template>
    <p 
      v-for="description in tooltipText"
      :key = description
      class="mb-1">
      {{description}}
    </p>
  </v-tooltip>
</template>

<script>
import * as d3 from "d3"

export default {
  props: {
    trendingTopicSentiment: {
      type: Array,
      required: true
    },
    sentimentGraphId: {
      type: String,
      required: true
    }
  },
  watch: {
    trendingTopicSentiment(val) {
      this.generateSentimentGraph(val)
    }
  },
  mounted() {
    this.generateSentimentGraph(this.trendingTopicSentiment)
  },
  computed: {
    tooltipText() {
      // console.log("=== start tooltipText() ===")

      // not able to change the tooltip basec on particular emotion or sentiment, can only combine all sentiments and emotions

      const objWithPercentage = this.getPercentageOfCount(this.trendingTopicSentiment)

      // console.log("objWithPercentage", objWithPercentage)

      const allDescriptions = []
      let description = ""

      for (const obj of objWithPercentage) {
        if (Object.prototype.hasOwnProperty.call(obj, 'emotion')) {
          description = `${obj.percentage}% of posts (${obj.count} posts) are associated with the emotion ${obj.emotion}`
        } else {
          description = `${obj.percentage}% of posts (${obj.count} posts) are associated with the sentiment ${obj.sentiment}`
        }
        // console.log("description", description)
        allDescriptions.push(description)
      }
      // console.log("allDescriptions", allDescriptions)
      return allDescriptions
    }
  },
  methods: {
    generateSentimentGraph(data) {
      // console.log("=== START generateSentimentGraph() === ")

      // console.log("test 0", this.sentimentGraphId)
      // console.log('test 1', d3.select(`#${this.sentimentGraphId}`))
      // console.log("test 2", d3.select(`#${this.sentimentGraphId}`)._groups)
      // console.log("test 3", d3.select(`#${this.sentimentGraphId}`)._groups[0])
      // console.log("test 4", d3.select(`#${this.sentimentGraphId}`)._groups[0][0])
      // console.log("test 5", d3.select(`#${this.sentimentGraphId}`)._groups[0][0].childNodes)
      // console.log("test 6", d3.select(`#${this.sentimentGraphId}`)._groups[0][0].childNodes.length)

      // only the first element disappears 
      // even without watching the value, when filters change, the svg of the first topic disappears, even though it is not the only topic with data changed
      if (d3.select(`#${this.sentimentGraphId}`)._groups[0][0].childNodes.length > 0) {
        d3.select(`#${this.sentimentGraphId}`).select("svg").remove();
      }

      // set the dimensions and margins of the graph
      // const margin = {top: 10, right: 10, bottom: 10, left: 10}
      // const width = 100 - margin.left - margin.right
      // const height = 33 - margin.top - margin.bottom
      const margin = {top: 0, right: 0, bottom: 0, left: 0}
      const width = 80
      const height = 6
      const x = d3.scaleLinear([0, 1], [margin.left, width - margin.right])
      // const formatPercent = x.tickFormat(null, "%")

      const stack = generateStack(data)
      // console.log("stack", stack)
      // console.log("x", x)
      // console.log("formatPercent", formatPercent)

      function generateStack(data) {
        // console.log("=== START generateStack() ===")
        // console.log("data", data)
        // console.log("sentiment object?", data.some(obj => Object.prototype.hasOwnProperty.call(obj, "sentiment")))
        // console.log("emotion object?", data.some(obj => Object.prototype.hasOwnProperty.call(obj, "emotion")))
        const isSentiment = data.some(obj => Object.prototype.hasOwnProperty.call(obj, "sentiment"))

        const total = d3.sum(data, d => d.count);
        let value = 0

        if (isSentiment) {
          return data.map(d => ({
            type: "sentiment",
            label: d.sentiment,
            value: d.count / total,
            startValue: value / total,
            endValue: (value += d.count) / total,
            count: d.count
          }));
        } else {
          return data.map(d => ({
            type: "emotion",
            label: d.emotion,
            value: d.count / total,
            startValue: value / total,
            endValue: (value += d.count) / total,
            count: d.count
          }));
        }
      }


      // append the svg object to the body of the page
      const svg = d3.select(`#${this.sentimentGraphId}`).append("svg")
        .attr("viewBox", [0, 0, width, height])
        .style("display", "block");
      // console.log("svg test", svg)

      svg.append("g")
        .attr("stroke", "white")
        .selectAll("rect")
        .data(stack)
        .join("rect")
        .attr("fill", function(d) { 
                // console.log("d", d)

                if (d.type === "sentiment") {
                  return d.label === "positive" ? "#EFB727" : (d.label === "negative" ? "#EB8159" : "#A0D6E8")
                  } else if (d.type === "emotion") {
                    return d.label === "anger" ? "#FB3412" : 
                      (d.label === "fear" ? "#8C56AF" :
                      (d.label === "joy" ? "#F7CF15" : 
                      (d.label === "neutral" ? "#a1a08d" : "#477BD1")))
                  }
                }
                
              )
        // rounded corners
        // .attr("rx", function(d) { 
        //         return d.label === "positive" ? "5" : (d.label === "negative" ? "5" : "0")
        //         })
        // .attr("ry", function(d) { 
        //         return d.label === "positive" ? "5" : (d.label === "negative" ? "5" : "0")
        //         })
        .attr("x", d => x(d.startValue))
        .attr("y", margin.top)
        .attr("width", d => x(d.endValue) - x(d.startValue))
        .attr("height", height - margin.top - margin.bottom)
        .append("title");
        // .text(d => `${formatPercent(d.value)} of posts (${d.count} posts) are associated with the ${d.type} ${d.label}`);

      // console.log("svg test 2", svg)


      // return svg.node();
      // console.log("=== END generateSentimentGraph() === ")
    },
    getPercentageOfCount(allCounts) {
      // console.log("=== START getPercentageOfCount() ===")
      // console.log("allCounts", allCounts)
      
      const total = d3.sum(allCounts, d => d.count)
      // console.log("total", total)

      for (const obj of allCounts) {
        // console.log("obj", obj)
        // console.log("obj.count / total", obj.count / total)
        obj.percentage = ((obj.count / total) * 100).toFixed(1)
      }

      return allCounts
    }
  }
}
</script>

<style>


</style>
