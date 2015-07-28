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
        int numLinks, numImages, numScripts, numStyles, numVotes;
        // Assumes that after splitting by "," we have following HN fields: 
        // id,url,score,num_links,num_images,num_scripts,num_styles,headers
        try {
            numLinks = Integer.parseInt(parts[3])
            numImages = Integer.parseInt(parts[4])
            numScripts = Integer.parseInt(parts[5])
            numStyles = Integer.parseInt(parts[6])
            numVotes = Integer.parseInt(parts[2]);
        } catch (NumberFormatException e) {
            return;
        }
        context.write(new IntWritable(numLinks), new IntWritable(numVotes));
    }
}