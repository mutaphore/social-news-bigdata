import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.sql.Timestamp;
import java.util.Date;


public class HourlyVoteCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {


    // get hour value from utc timestamp
    private int getHour(Long timestamp) {
        java.util.Date date= new java.util.Date(timestamp* 1000);
        return date.getHours();
    }

    private int getNumVotes(String line) {
        String[] parts = line.split(",");
        if (parts.length != 9) {
            return 0;
        }
        try {
            return Integer.parseInt(parts[1]);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    @Override
    public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        String line = value.toString(); 
        String[] parts = line.split(",");
        // Assumes that after splitting by "," we have following Reddit fields: 
        // id, score, title, url, author, num_comments, created_utc, subreddit, domain
        int hour = getHour((long)Double.parseDouble(parts[6]));
        int numVotes = getNumVotes(line);
        
        context.write(new Text(Integer.toString(hour)), new IntWritable(numVotes));
    }
}
