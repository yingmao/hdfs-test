package hdfs.test;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class CreateDir
{
    public static void main( String[] args ) throws Exception
    {
        if(args.length < 1){
            System.out.println("Invalid dir name");
            return;
        }
        String dirName = args[0];
        FileSystem fs = FileSystem.get(Config.getHdfsConfig());
        fs.mkdirs(new Path(dirName));
        fs.close();
        System.out.println("Create Dir success!");
    }
}