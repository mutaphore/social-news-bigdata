import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class VoteCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private int getNumComments(String line) {
        String[] items = line.split(",");
        // Number of comments is the last item
        return Integer.parseInt(items[items.length-1]);
    }

    private int getNumVotes(String line) {
        StringTokenizer tokenizer = new StringTokenizer(line, ",");
    }

    private List<String> lineParse(String line) {
        List<String> items = new List<String>();

        // Check if we have a valid line
        try {
            Integer.parseInt(line.split(",")[0]);
        } catch(NumberFormatException) {
            return null;
        }

        Pattern pattern = Pattern.compile("\\s*(\"[^\"]*\"|[^,]*)\\s*");
        Matcher matcher = pattern.matcher(line);
        while (matcher.find()) {
            items.add(matcher.group(1));
        }
        // Check if we got all the fields
        if (items.size() != 14) {
            return null;
        }
        
    }

    @Override
    public void map(LongWritable key, Text value, Context context) {
        String line = value.toString(); 
        i
    }
}