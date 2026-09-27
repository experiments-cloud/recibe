(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable d)
    (clear a)
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
