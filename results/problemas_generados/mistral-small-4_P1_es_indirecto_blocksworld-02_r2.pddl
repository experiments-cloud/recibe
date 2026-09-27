(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable d)
    (clear a)
    (clear b)
    (clear c)
    (clear d)
    (handempty)
    (on c b)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
