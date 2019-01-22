package hdfs.test;

import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.LocatedFileStatus;
import org.apache.hadoop.fs.Path;

public class ListFiles {

    public static void main( String[] args ) throws Exception
    {
        if(args.length < 1){
            System.out.println("Invalid dir name");
            return;
        }
        String dirName = args[0];
        FileSystem fs = FileSystem.get(Config.getHdfsConfig());
        if(!fs.exists(new Path(dirName))){
            System.out.println(dirName + " Not found!!!");
            return;
        }
        System.out.println("==========  List files in path:" + dirName + "  =============");
        FileStatus[] fileStatuses = fs.listStatus(new Path(dirName));
        for(FileStatus fileStatus : fileStatuses){
            if (fileStatus.isDirectory()){
                System.out.println("Dictionary - " + fileStatus.getPath().getName());
            }else{
                System.out.println("File - " + fileStatus.getPath().getName());
            }
        }
        fs.close();
        System.out.println(">>>>>>>>>>>>  List files in path:" + dirName + " <<<<<<<<<<<");
    }
}
