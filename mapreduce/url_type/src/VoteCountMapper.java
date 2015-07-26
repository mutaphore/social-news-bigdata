import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class VoteCountMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {

    private int getNumComments(String line) {
        String[] items = line.split(",");
        // Number of comments is the last item
        return Integer.parseInt(items[items.length-1]);
    }

    private int getNumVotes(String line) {
        StringTokenizer tokenizer = new StringTokenizer(line, ",");
    }

    @Override
    public void map(LongWritable key, Text value, Context context) {
        String line = value.toString(); 
        String[] parts = line.split(",");
        // HN Fields: id, type, author(by), time, text, url, score, title, descendants
        int numComments = Integer.parseInt(parts[8]);
        int numVotes = Integer.parseInt(parts[6]);
        context.write(new IntWritable(numComments), new IntWritable(numVotes));
    }
}