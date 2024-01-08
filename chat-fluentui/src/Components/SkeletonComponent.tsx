
import {
    Skeleton,
    SkeletonItem,
  } from "@fluentui/react-components";
import * as Styles from "./styles";


const SkeletonComponent = () => {
    const classes = Styles.useSkeletonStyles();
    return (
        
        <Skeleton>
        <div className={classes.firstRow}>
          <SkeletonItem shape="circle" size={8} />
          <SkeletonItem shape="rectangle" size={8} />
        </div>
        <div className={classes.secondThirdRow}>
          <SkeletonItem shape="circle" size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
        </div>
        <div className={classes.secondThirdRow}>
          <SkeletonItem shape="square" size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
          <SkeletonItem size={8} />
        </div>
      </Skeleton>
    )
}

export default SkeletonComponent;
