import java.util.*;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable; 
import org.apache.hadoop.io.LongWritable; 
import org.apache.hadoop.io.ArrayWritable; 
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class VoteCountMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {

    @Override
    public void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        String line = value.toString(); 
        String[] parts = line.split(",");
        int numComments, numVotes;
        // Assumes that after splitting by "," we have following HN fields: 
        // id, type, author(by), time, text, url, score, title, descendants
        try {
            numComments = Integer.parseInt(parts[8]);
            numVotes = Integer.parseInt(parts[6]);
        } catch (NumberFormatException e) {
            return;
        }
        context.write(new IntWritable(numComments), new IntWritable(numVotes));
    }
}