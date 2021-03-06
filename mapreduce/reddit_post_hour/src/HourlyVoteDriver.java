import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class HourlyVoteCountDriver {

    public static void main(String[] args) throws Exception{

        if (args.length != 2) {
            System.err.println("Usage: HourlyVoteCountDriver <input path> <output path>");
            System.exit(-1);
        }

        Job job = new Job();

        job.setJarByClass(HourlyVoteCountDriver.class);
        job.setJobName("HourlyVoteCount");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(HourlyVoteCountMapper.class);
        job.setReducerClass(HourlyVoteCountReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FloatWritable.class);
        
        job.setOutputFormatClass(CsvOutputFormat.class);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}
